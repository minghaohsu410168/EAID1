# EAID1
**請先確認有將D1的ROS_MASTER_URI設為自己server的ip以及連到基地的IOT_2.4G網路**  
  
## 新增工作區
`$mkdir -p catkin_ws/src`  
將所有套件解接壓縮至src內後編譯  
`$catkin_make`  
執行roscore  
<img src="https://github.com/minghaohsu410168/EAID1/blob/master/roscore.png" width=500 />  
有出現以上畫面代表有成功開啟 ROS master  

## 啟動EAID1
ssh遠端進入EAID1(兩台D1 ip為10.87.1.120 / 10.87.1.121)  
`$ssh eaid1@10.87.1.121`  
<img src="https://github.com/minghaohsu410168/EAID1/blob/Desktop/d1_ssh.png" width=500 />  
盡量先校正時間，之後才不容易出錯。  
`$sudo ntpdate tock.stdtime.gov.tw`  
若出現錯誤，可以用基地架的ntp server，以下擇一即可。  
`$sudo ntpdate 10.87.1.116` / 
`$sudo ntpdate 10.10.100.160`  
執行bringup.launch，啟動D1  
`$roslaunch dashgo_bringup bringup.launch`  
<img src="https://github.com/minghaohsu410168/EAID1/blob/Desktop/d1_launch.png" width=500 />  
## teleop控制
啟動D1後可以先用方向鍵控制看看馬達有沒有問題。  
```
$sudo apt install ros-melodic-turtlebot3-teleop
$roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```
<img src="https://github.com/minghaohsu410168/EAID1/blob/Desktop/teleop_error.png" width=500 />   
第一次會出現錯誤，因為需要引入TURTLEBOT3的模型，可在bashrc中新增

```
$echo "export TURTLEBOT3_MODEL=waffle_pi" >> .bashrc 
$source .bashrc 
```
再次執行`$roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch`即可以w,a,s,d,x鍵控制D1  
<img src="https://github.com/minghaohsu410168/EAID1/blob/Desktop/teleop.png" width=500 />  

## Navigation
確認沒問題後可以開始D1的導航  
`$roslaunch dashgo_nav navigation_airobot.launch`  
<img src="https://github.com/minghaohsu410168/EAID1/blob/Desktop/nav_error.png" width=500 />  
出現的錯誤為缺少執行需要的套件，需要額外安裝以下套件  
```
$sudo apt install ros-melodic-amcl
$sudo apt install ros-melodic-move-base
$sudo apt install ros-melodic-global-planner
$sudo apt install ros-melodic-teb-local-planner
```
完成安裝後即可再次執行navigation的launch檔  
<img src="https://github.com/minghaohsu410168/EAID1/blob/Desktop/nav.png" width=500 />  
在rviz畫面上方工具列會用到**2D Pose Estimate**和**2D Nav Goal**兩個按鈕  
**2D Pose Estimate**給予D1的起始定位，而**2D Nav Goal**給予D1目標點。  
還沒寫完...
## SLAM

