#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include <vector>
#include <string>

class JointStatePublisher : public rclcpp::Node
{
public:
  JointStatePublisher()
  : Node("joint_state_publisher"), count_(0)
  {
    publisher_ = this->create_publisher<sensor_msgs::msg::JointState>("joint_states", 10);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100), std::bind(&JointStatePublisher::timer_callback, this));
    joint_positions_ = {0, 0, 0};  // Default joint positions
  }

  void set_joint_positions(std::vector<double> positions) {
    joint_positions_ = positions;
  }

private:
  void timer_callback()
  {
    auto message = sensor_msgs::msg::JointState();
    message.header.stamp = this->now();
    message.name = {"X", "Y", "Z"};
    message.position = joint_positions_;  // Use your joint positions
    publisher_->publish(message);
    count_++;
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr publisher_;
  size_t count_;
  std::vector<double> joint_positions_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto joint_state_publisher = std::make_shared<JointStatePublisher>();

  // Set joint positions based on user input
  std::string input;
  while (true) {
    std::cout << "Enter joint positions (comma-separated) or 'q' to quit: ";
    std::getline(std::cin, input);
    if (input == "q") {
      break;
    }
    std::istringstream ss(input);
    std::string token;
    std::vector<double> joint_positions;
    while(std::getline(ss, token, ',')) {
      joint_positions.push_back(std::stod(token));
    }
    joint_state_publisher->set_joint_positions(joint_positions);
  }

  rclcpp::spin(joint_state_publisher);
  rclcpp::shutdown();
  return 0;
}
