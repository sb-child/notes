# PipeWire

[返回](README.md)

## 配置文件们

### PipeWire

```text
/home/sbchild/.config/pipewire/pipewire.conf.d/01.conf
```

### Wireplumber

```text
/home/sbchild/.config/wireplumber/wireplumber.conf.d/51-alsa-pro-audio.conf
```

## 创建虚拟麦克风

```bash
pactl load-module module-null-sink media.class=Audio/Source/Virtual sink_name=virt-mic channel_map=front-left,front-right
```

## 创建虚拟输出

```bash
pactl load-module module-null-sink media.class=Audio/Sink sink_name=virt-output channel_map=front-left,front-right
```

## 远程输出

### 电脑 -> 手机(Termux)

手机:

```bash
mkdir /data/data/com.termux/files/usr/etc/pulse/default.pa.d/
echo "load-module module-native-protocol-tcp auth-ip-acl=电脑IP auth-anonymous=true" > /data/data/com.termux/files/usr/etc/pulse/default.pa.d/my.pa
# pulseaudio 会在 0.0.0.0 监听 tcp:4713 端口
pulseaudio
```

电脑:

```bash
# 确保手机端 pulseaudio 处于运行状态
pactl load-module module-tunnel-sink server=tcp:手机IP
```
