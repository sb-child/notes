# Pipewire

## 创建虚拟麦克风

```bash
pactl load-module module-null-sink media.class=Audio/Source/Virtual sink_name=virt-mic channel_map=front-left,front-right
```
