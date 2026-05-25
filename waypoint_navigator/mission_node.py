import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import String
import yaml
import time


class MissionNode(Node):
    def __init__(self):
        super().__init__('mission_node')

        # --- Parâmetros ---
        self.declare_parameter('waypoints_file', '')
        self.declare_parameter('max_retries', 3)

        self.max_retries = self.get_parameter('max_retries').value
        waypoints_file = self.get_parameter('waypoints_file').value

        # --- Variáveis de estado ---
        self.pose_inicial = None
        self.waypoints = []

        # --- Publisher de status da missão ---
        self.status_pub = self.create_publisher(String, '/mission/status', 10)

        # --- Action client do Nav2 ---
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # --- Subscriber pra capturar pose inicial ---
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.cb_pose_inicial,
            10
        )

        # --- Carrega waypoints do YAML ---
        if waypoints_file:
            self.waypoints = self.carregar_waypoints(waypoints_file)
        else:
            self.get_logger().error('Nenhum arquivo de waypoints informado!')
            return

        self.get_logger().info(f'{len(self.waypoints)} waypoints carregados.')
        self.get_logger().info('Aguardando pose inicial do AMCL...')

    def cb_pose_inicial(self, msg):
        # Captura a pose inicial apenas uma vez e inicia a missão
        if self.pose_inicial is None:
            self.pose_inicial = msg.pose.pose
            self.get_logger().info('Pose inicial capturada. Iniciando missão...')
            self.pose_sub = None  # Para de escutar
            self.executar_missao()

    def carregar_waypoints(self, caminho):
        with open(caminho, 'r') as f:
            dados = yaml.safe_load(f)

        waypoints = []
        for wp in dados['waypoints']:
            pose = NavigateToPose.Goal()
            pose.pose.header.frame_id = 'map'
            pose.pose.pose.position.x = wp['x']
            pose.pose.pose.position.y = wp['y']
            pose.pose.pose.orientation.z = wp.get('oz', 0.0)
            pose.pose.pose.orientation.w = wp.get('ow', 1.0)
            waypoints.append((wp.get('nome', 'sem_nome'), pose))

        return waypoints

    def publicar_status(self, msg):
        self.get_logger().info(msg)
        status = String()
        status.data = msg
        self.status_pub.publish(status)

    def executar_missao(self):
        # Navega por cada waypoint
        for i, (nome, goal) in enumerate(self.waypoints):
            self.publicar_status(f'[{i+1}/{len(self.waypoints)}] Indo para: {nome}')
            sucesso = self.navegar(goal)

            if sucesso:
                self.publicar_status(f'Waypoint "{nome}" concluído.')
            else:
                self.publicar_status(f'Waypoint "{nome}" falhou após tentativas. Pulando...')

        # Retorna à posição inicial
        self.publicar_status('Todos os waypoints visitados. Retornando à posição inicial...')
        self.retornar_origem()

    def navegar(self, goal):
        # Aguarda o servidor Nav2 estar disponível
        self.nav_client.wait_for_server()

        for tentativa in range(1, self.max_retries + 1):
            self.get_logger().info(f'Tentativa {tentativa}/{self.max_retries}...')

            # Atualiza o timestamp do goal
            goal.pose.header.stamp = self.get_clock().now().to_msg()

            # Envia o goal e aguarda resultado
            future = self.nav_client.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future)
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().warn('Goal rejeitado pelo Nav2.')
                continue

            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            status = result_future.result().status

            # Status 4 = SUCCEEDED no ROS2 action
            if status == 4:
                return True
            else:
                self.get_logger().warn(f'Navegação falhou com status {status}. Tentando novamente...')
                time.sleep(1.0)

        return False

    def retornar_origem(self):
        # Monta goal com a pose inicial capturada no começo
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose = self.pose_inicial

        sucesso = self.navegar(goal)

        if sucesso:
            self.publicar_status('Missão concluída! Robô retornou à origem.')
        else:
            self.publicar_status('Falha ao retornar à origem.')


def main(args=None):
    rclpy.init(args=args)
    node = MissionNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()