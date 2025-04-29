import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

class EqualInclinationInterference:
    """
    单色发光面引起的等倾干涉图样模拟
    
    参数说明:
    - wavelength: 光波波长 (nm)
    - refractive_index: 介质折射率
    - thickness: 薄膜厚度 (nm)
    - incidence_angle_range: 入射角范围 (度)
    - intensity_max: 最大光强
    - resolution: 图像分辨率
    """
    def __init__(self, wavelength=632.8, refractive_index=1, thickness=1000, 
                 incidence_angle_range=30, intensity_max=1, resolution=500):
        self.wavelength = wavelength  # 波长 (nm)
        self.refractive_index = refractive_index  # 折射率
        self.thickness = thickness  # 薄膜厚度 (nm)
        self.incidence_angle_range = incidence_angle_range  # 入射角范围 (度)
        self.intensity_max = intensity_max  # 最大光强
        self.resolution = resolution  # 图像分辨率
        
        # 创建图形和轴
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.3)
        
        # 创建滑块轴
        self.ax_wavelength = plt.axes([0.2, 0.20, 0.6, 0.03])
        self.ax_thickness = plt.axes([0.2, 0.15, 0.6, 0.03])
        self.ax_refractive = plt.axes([0.2, 0.10, 0.6, 0.03])
        self.ax_angle = plt.axes([0.2, 0.05, 0.6, 0.03])
        
        # 创建滑块
        self.slider_wavelength = Slider(self.ax_wavelength, 'λ (nm)', 400, 800, valinit=wavelength)
        self.slider_thickness = Slider(self.ax_thickness, 'd (nm)', 100, 5000, valinit=thickness)
        self.slider_refractive = Slider(self.ax_refractive, 'n', 1.0, 2.0, valinit=refractive_index)
        self.slider_angle = Slider(self.ax_angle, 'rad (°)', 5, 60, valinit=incidence_angle_range)
        
        # 添加重置按钮
        resetax = plt.axes([0.8, 0.25, 0.1, 0.04])
        self.button = Button(resetax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')
        
        # 初始化图像
        self.img = self.ax.imshow(self._calculate_pattern(), cmap='gray', 
                                 extent=[-incidence_angle_range, incidence_angle_range, 
                                        -incidence_angle_range, incidence_angle_range])
        self.ax.set_xlabel('rad X (°)')
        self.ax.set_ylabel('rad Y (°)')
        self.ax.set_title('Example')
        
        # 添加颜色条
        plt.colorbar(self.img, ax=self.ax, label='I(cd)')
        
        # 设置滑块回调函数
        self.slider_wavelength.on_changed(self.update)
        self.slider_thickness.on_changed(self.update)
        self.slider_refractive.on_changed(self.update)
        self.slider_angle.on_changed(self.update)
        self.button.on_clicked(self.reset)
        
    def _calculate_pattern(self):
        """计算干涉图样"""
        # 创建角度网格
        x = np.linspace(-self.incidence_angle_range, self.incidence_angle_range, self.resolution)
        y = np.linspace(-self.incidence_angle_range, self.incidence_angle_range, self.resolution)
        X, Y = np.meshgrid(x, y)
        
        # 计算入射角 (从法线算起)
        theta = np.sqrt(X**2 + Y**2)  # 角度(度)
        theta_rad = np.radians(theta)  # 转换为弧度
        
        # 计算光程差引起的相位差
        delta = 4 * np.pi * self.refractive_index * self.thickness * np.cos(theta_rad) / self.wavelength
        
        # 计算干涉光强 (假设两束光振幅相同)
        intensity = self.intensity_max * (1 + np.cos(delta))
        
        return intensity
    
    def update(self, val):
        """更新图像"""
        self.wavelength = self.slider_wavelength.val
        self.thickness = self.slider_thickness.val
        self.refractive_index = self.slider_refractive.val
        self.incidence_angle_range = self.slider_angle.val
        
        # 更新图像数据
        self.img.set_data(self._calculate_pattern())
        self.img.set_extent([-self.incidence_angle_range, self.incidence_angle_range, 
                           -self.incidence_angle_range, self.incidence_angle_range])
        self.fig.canvas.draw_idle()
    
    def reset(self, event):
        """重置参数"""
        self.slider_wavelength.reset()
        self.slider_thickness.reset()
        self.slider_refractive.reset()
        self.slider_angle.reset()
    
    def show_static(self):
        """显示静态图像"""
        plt.show()
    
    def animate(self, frames=30):
        """创建动态动画"""
        def update_frame(frame):
            # 动态改变薄膜厚度
            self.thickness = 100 + 4900 * (0.5 + 0.5 * np.sin(frame * 2 * np.pi / frames))
            self.slider_thickness.set_val(self.thickness)
            return self.img,
        
        # 创建动画
        ani = FuncAnimation(self.fig, update_frame, frames=frames, 
                           interval=100, blit=True)
        return ani

# 使用示例
if __name__ == "__main__":
    # 创建干涉模拟器实例
    interference = EqualInclinationInterference(
        wavelength=632.8,  # He-Ne激光波长
        refractive_index=1,  # 类似水的折射率
        thickness=1500,  # 薄膜厚度
        incidence_angle_range=60,  # 角度范围
        resolution=500  # 图像分辨率
    )
    
    # 显示静态图像
    print("显示静态干涉图样...")
    interference.show_static()
    
    # 如果要运行动态模式，取消下面的注释
    # print("运行动态模式...")
    # ani = interference.animate(frames=60)
    # plt.show()
