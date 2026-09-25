# Maps and distant terrain

The beta adds MapSyncer 1.0.4beta1 on clients and servers. It shares maps of generated
terrain, including pregenerated areas nobody has visited. It does not share
waypoints or generate missing Minecraft chunks. Map caches stay outside the pack.

New clients use `mapRegionLoadIntervalTicks = 0`. The full synchronized map is
still downloaded and saved, but only regions within the player's current view
distance are immediately loaded into Xaero. Distant regions load from disk when
needed instead of being queued together after a large first sync. Existing clients
should make the same change in `config/mapsyncer-client.toml` while Minecraft is
closed. Players may later choose a positive interval if they want gradual background
loading; `20` loads one distant region per second, while the upstream default `1`
loads up to twenty per second.

## Set up map sharing

Update the stopped server through Packwiz. For an existing world, copy
`defaultconfigs/mapsyncer-server.toml` to `<world>/serverconfig/mapsyncer-server.toml`
before starting. If that file already exists, back it up and change only
`incrementalUpdateMode = "TICK"` and `incrementalUpdateIntervalTicks = 6000`
under `[incremental_update]`. New worlds receive the defaults automatically.

Start through AMP. In its Minecraft console, run:

```text
mapsyncer generate
mapsyncer status
```

This builds maps from saved world regions. DH-only LOD generation is not a
substitute for full Minecraft chunks. Changed regions are checked every 6000
ticks (about five minutes at 20 TPS). Clients check for newer maps on joining;
use `/mapsyncer sync all` in game to request them manually.

MapSyncer's transfer limit stays at 1024 KB/s and conversion concurrency at four.
Other scan settings use the release's defaults. Back up personal maps before
trying the beta; map merging and reconnect behavior await in-game testing.

## Faster DH loading

New installations use four DH threads at a 0.75 runtime ratio. This shared
client/server default preserves existing settings. For the previous allocation
on a new server, use two threads and a 0.5 ratio.

For an existing client, close Minecraft and edit these values in
`config/DistantHorizons.toml`:

```toml
[common.multiThreading]
numberOfThreads = 4
threadRunTimeRatio = 0.75
```

On the stopped server, remove DH transfer caps by changing these values under
its existing `[server]` section. Leave its CPU settings alone:

```toml
playerBandwidthLimit = 0
globalBandwidthLimit = 0
```

Zero disables the bandwidth caps. Request-rate controls keep upstream defaults.
Disk access, LOD availability and client processing still affect speed. Edit the
named keys without duplicating TOML sections or replacing server IDs. The pack
keeps PRE_EXISTING_ONLY generation and radius 128.

New beta Prism imports use a 12 GiB maximum heap. Existing instances need that
memory change made in Prism; Packwiz cannot update launcher settings.
