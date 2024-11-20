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
