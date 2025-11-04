# osu!

一款音游，但是... 但是我在说 `osu!lazer` 而不是 `osu!stable`

然后这个指南一般只针对 Linux 系统，确切来说我在用 Fedora 做示范。

[返回](../README.md)

## Pipewire 与音频延迟

想必你也是厌倦了 audio offset 到底该怎么调...

我已经替你蹚过浑水了，以下是你需要做的事情：

### 1. Pipewire 设置

创建 `~/.config/pipewire/pipewire.conf.d/custom.conf` 然后这是最精简的文件内容:

```conf
context.properties = {
    default.clock.rate          = 48000
    default.clock.allowed-rates = [ 44100, 48000, 96000, 192000, 384000 ]
    default.clock.quantum       = 32
    default.clock.min-quantum   = 16
    default.clock.max-quantum   = 64
    default.clock.quantum-limit = 64
}
context.modules = []
context.objects = []
context.exec = []
```

然后重启 Pipewire 服务:

```bash
$ systemctl restart --user pipewire.service
```

### 2. 关于 osu! 这边的事情

我建议你去[这里](https://github.com/ppy/osu/releases)下载 `osu.AppImage` 而不是在 flatpak 安装。

然后记住一个很魔法的环境变量: `PIPEWIRE_LATENCY=<quantum>/<rate>`，以后要考！

最后，记得在游戏内设置 `Audio > Devices > Output device` 为 `Pipewire Sound Server`。

### 3. 采样率和缓冲区

接下来是重头戏了。在你游玩之前一定要做这些事：

#### 3.1 降低采样率

其实 osu! 在用 44100 Hz 的采样率。

但如果声卡工作在其他采样率呢，则会带来重采样(resampling)的开销。

为了不让重采样后的音频爆炸，是需要用更大的缓冲区作为代价的。

想要强制声卡工作在 44100 Hz 采样率，你可以这样做:

```bash
$ pw-metadata -n settings 0 clock.force-rate 44100
```

然后如果你想撤销这个设置，你可以这样:

```bash
$ pw-metadata -n settings 0 -d clock.force-rate
```

#### 3.2 缩小缓冲区

其实 osu! 的默认 `quantum` 是 441 采样。

更大的缓冲区可以降低 CPU 负载，并减少爆音的概率，但是会增加延迟...

Pipewire 中的 `quantum` 参数代表了缓冲区大小，单位是采样。

为什么会爆音呢？它有两种情况：

- 要播放音频的客户端迟到了，在输出缓冲区空了之后才来得及往里塞采样。
- 客户端来早了，或者输出缓冲区仍然是满的，往里塞的新采样被丢弃了。

小小的缓冲区可以迫使客户端更频繁的往里塞采样，这样可以让 hit sound 播放的更及时，timing 更精确。

想要强制声卡的缓冲区为 16 采样，你可以这样做:

```bash
$ pw-metadata -n settings 0 clock.force-quantum 16
```

然后如果你想撤销这个设置，你可以这样:

```bash
$ pw-metadata -n settings 0 -d clock.force-quantum
```

### 4. 游玩须知

上面说过了 `PIPEWIRE_LATENCY=<quantum>/<rate>` 环境变量，接下来就是它的用武之地:

```bash
PIPEWIRE_LATENCY=16/44100 ./osu.AppImage
```

为了验证它真的在工作，你可以用 `pw-top` 看一下:

<div style="overflow-x: scroll; white-space: nowrap;">

| S   | ID  | QUANT | RATE  | WAIT   | BUSY  | W/Q  | B/Q  | ERR   | FORMAT        | NAME                                                                |
| --- | --- | ----- | ----- | ------ | ----- | ---- | ---- | ----- | ------------- | ------------------------------------------------------------------- |
| S   | 29  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | Dummy-Driver                                                        |
| S   | 30  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | Freewheel-Driver                                                    |
| S   | 49  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | Midi-Bridge                                                         |
| S   | 52  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | bluez_midi.server                                                   |
| R   | 55  | 16    | 44100 | 20.5us | 3.8us | 0.06 | 0.01 | 239   | S32LE 2 44100 | alsa_output.usb-iBasso_Macaron-01.analog-stereo                     |
| R   | 94  | 64    | 48000 | 9.6us  | 4.3us | 0.03 | 0.01 | 11125 | F32LE 2 48000 | + Chromium                                                          |
| R   | 158 | 16    | 44100 | 9.6us  | 2.8us | 0.03 | 0.01 | 11530 | F32LE 2 44100 | + alsa_playback.osu!                                                |
| S   | 43  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | alsa_input.pci-0000_04_00.5-platform-acp_pdm_mach.0.stereo-fallback |
| S   | 56  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | alsa_output.pci-0000_04_00.6.analog-stereo                          |
| S   | 57  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | alsa_input.pci-0000_04_00.6.analog-stereo                           |
| S   | 73  | 0     | 0     | ---    | ---   | ---  | ---  | 0     |               | v4l2_input.pci-0000_04_00.3-usb-0_3_1.0                             |
| I   | 76  | 0     | 0     | 0.0us  | 0.0us | ???  | ???  | 0     | S16LE 1 44100 | speech-dispatcher-dummy                                             |

</div>

把 `Audio > Offset Adjustment > Audio offset` 拉到 0 ms，打几个谱试试吧！

### 5. Showcase

打开这三个 Mod，然后闭上眼睛，跟随着**节拍器**，用你更灵活的惯用手戳键盘吧！\
尽可能让你 tap 的**相位**和节拍器**保持一致**，这很重要！

- `Target Practice` (Seed: 0)
- `Magnetised` (Attraction strength: 1.0)
- `Muted` (Final volume at combo: 1)

---

**这部分还在施工，敬请期待。**

> 以下表格中，**负数**偏移代表 early，**正数**偏移代表 late。\
> 平均值算法是我[临时起意](./latency-analyze.py)写的。

<div style="overflow-x: scroll; white-space: nowrap;">

| ID              | 输出缓冲区/采样率 | 游戏缓冲区/采样率 | 平均偏移(ms) | 平均 UR(0.1ms) | 样本数 |
| --------------- | ----------------- | ----------------- | ------------ | -------------- | ------ |
| [1](data-1.txt) | 16/44100          | 16/44100          | -21.98       | 181.82         | 1      |

</div>

## 正确的调节 Audio offset

**这部分还在施工，敬请期待。**
