# Linux 日常

## Fedora - 清理旧软件包

```bash
sudo dnf remove --oldinstallonly
```

## Fedora - usbip

- 参考: https://developer.ridgerun.com/wiki/index.php?title=How_to_setup_and_use_USB/IP

### 服务端

```bash
sudo modprobe usbip_host
sudo systemctl start usbip-server.service
```

需要开放 `tcp:3240` 端口

#### 查看当前已连接的设备

```bash
$ usbip list -l

 - busid 3-10 (8087:0026)
   Intel Corp. : AX201 Bluetooth (8087:0026)

 - busid 3-3.3 (3533:5c15)
   unknown vendor : unknown product (3533:5c15)

...
```

#### 分享设备

```bash
sudo usbip bind -b <busid>
```

#### 取消分享设备

```bash
sudo usbip unbind -b <busid>
```

### 客户端

```bash
sudo modprobe vhci-hcd
```

#### 列出服务端分享的设备

```bash
usbip list -r <服务端ip>
```

#### 挂载服务端分享的设备

```bash
sudo usbip attach -r <服务端ip> -b <busid>
```

#### 列出已经挂载的设备

```bash
$ sudo usbip port

Imported USB devices
====================
Port 00: <Port in Use> at Full Speed(12Mbps)
       unknown vendor : unknown product (3533:5c15)
       5-1 -> usbip://192.168.11.30:3240/3-3.3
           -> remote bus/dev 003/008
```

#### 卸载设备

```bash
sudo usbip detach -p <port>
```
