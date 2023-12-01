import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from rclpy.qos import QoSProfile

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        qos_profile = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(JointState, 'joint_states', qos_profile)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count_ = 0
        self.joint_positions = [0, 0, 0]  # Default joint positions

    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["X", "Y", "Z"]
        msg.position = self.joint_positions
        self.publisher_.publish(msg)
        self.count_ += 1

    def set_joint_positions(self, positions):
        self.joint_positions = positions

def main(args=None):
    rclpy.init(args=args)
    joint_state_publisher = JointStatePublisher()
    # Set joint positions based on user input
    user_input = input("Enter joint positions (comma-separated): ")
    joint_positions = list(map(float, user_input.split(',')))
    joint_state_publisher.set_joint_positions(joint_positions)
    rclpy.spin(joint_state_publisher)
    joint_state_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
