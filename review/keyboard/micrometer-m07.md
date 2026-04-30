# Micrometer M07

披着磁轴与 Rapid Trigger 的外壳，实际 SMT 质检不到位。

[返回](../README.md)

## 官方资料

- [使用说明](https://www.yuque.com/qiguohaixiudebaikou/uorqwd)
- [图纸](https://pan.baidu.com/s/1yW-PEgEa0BJYkv8tY4prwg?pwd=8bpg)
- [仓库(提issue)](https://github.com/RQNG/Micrometer-M07)

## 初体验

屏幕排线只应该塞进 FPC 座子一点点就刚好锁住，这是预期的，但强度可能不够。

到手一定先看看单片机是不是虚焊了，避免带来不必要的麻烦。

如果轴塞不进去，应该用锉刀给轴的四边磨掉一些，我担心铝板变形。

初次开机，记得长按旋钮，进入设置：

- 在波形显示菜单，依次选择按键观察波形。按下按键，向上波动为 M0，向下波动为 M1。
- 在按键自定义菜单，依次选择按键，选择磁性(M0/M1)，设置键程(单位 0.01mm)，然后校准。设置 Rapid Trigger 参数，通常保持默认即可。设置 Key Code，如果不需要这个按键则选择 Disabled。
- 然后翻到 RT Result 测试你的触发设置。
- 退回到设置，往后翻，选择保存。
- 翻到第一个选项，退出设置。

## 设备特征

接口: USB(Full Speed, 0483:5740)

<details><summary><code>lsusb -vvv</code></summary>

```
Bus 001 Device 012: ID 0483:5740 STMicroelectronics Virtual COM Port
Couldn't open device, some information will be missing
Negotiated speed: Full Speed (12Mbps)
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               2.00
  bDeviceClass            0 [unknown]
  bDeviceSubClass         0 [unknown]
  bDeviceProtocol         0
  bMaxPacketSize0        64
  idVendor           0x0483 STMicroelectronics
  idProduct          0x5740 Virtual COM Port
  bcdDevice            2.00
  iManufacturer           1 STMicroelectronics
  iProduct                2 BLUEPILL_F103CB HID in FS Mode
  iSerial                 3 4E7F30A04800
  bNumConfigurations      1
  Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength       0x003b
    bNumInterfaces          2
    bConfigurationValue     1
    iConfiguration          0
    bmAttributes         0xc0
      Self Powered
    MaxPower              100mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      1 Boot Interface Subclass
      bInterfaceProtocol      2 Mouse
      iInterface              0
        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.11
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 (null)
          wDescriptorLength      74
          Report Descriptors:
            ** UNAVAILABLE **
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x81  EP 1 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0004  1x 4 bytes
        bInterval              10
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        1
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      1 Boot Interface Subclass
      bInterfaceProtocol      1 Keyboard
      iInterface              0
        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.11
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 (null)
          wDescriptorLength      45
          Report Descriptors:
            ** UNAVAILABLE **
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x82  EP 2 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval              10
```

</details>

## 性能指标

**条件: USB, Rapid Trigger 默认设置**

| Key                | Value       |
| ------------------ | ----------- |
| Resolution         | 125Hz (8ms) |
| Hold Time          | ≥ 16ms      |
| keystroke Interval | ≥ 16ms      |

这组数据有多么可怕，两个键尽可能同时按，它也能分出先后，加上 `16+(8n)`ms 的间隔。
