# Maps and distant terrain

The beta includes MapSyncer 1.0.4beta1 on clients and servers. It shares maps of generated
terrain, including pregenerated areas nobody has visited. It does not share
waypoints or generate missing Minecraft chunks. Map caches stay outside the pack.

New clients disable automatic synchronization with `[client] autoSyncEnabled = false`
and use `mapRegionLoadIntervalTicks = 0` for manually synchronized maps. The full synchronized map is
still downloaded and saved, but only regions within the player's current view
distance are immediately loaded into Xaero. Distant regions load from disk when
needed instead of being queued together after a large first sync. Existing clients
should make the same change in `config/mapsyncer-client.toml` while Minecraft is
closed. Players may later choose a positive interval if they want gradual background
loading; `20` loads one distant region per second, while the upstream default `1`
loads up to twenty per second.

## Set up map sharing

Update the stopped server through Packwiz. New worlds receive
`[incremental_update] incrementalUpdateMode = "DISABLED"` from
`defaultconfigs/mapsyncer-server.toml`. For an existing world, back up
`<world>/serverconfig/mapsyncer-server.toml` and set that value to `"DISABLED"`
without replacing other settings. The retained 6000-tick interval is inactive
while incremental updates are disabled.

Start through AMP. In its Minecraft console, run:

```text
mapsyncer generate
mapsyncer status
```

This builds maps from saved world regions. DH-only LOD generation is not a
substitute for full Minecraft chunks. Automatic client synchronization and server
incremental updates are disabled by default; use `/mapsyncer sync all` in game
to request maps manually. Existing clients can use `/mapsyncer autosync off` or
set `[client] autoSyncEnabled = false` in their preserved client configuration.

MapSyncer's transfer limit stays at 1024 KB/s and conversion concurrency at four.
Other scan settings use the release's defaults. Back up personal maps before
trying the beta; map merging and reconnect behavior await in-game testing.

## Faster DH loading

New installations use four DH threads at a 0.50 runtime ratio. This shared
client/server default preserves existing settings. To reduce CPU use, fewer threads or a lower runtime ratio can be chosen locally.

For an existing client, close Minecraft and edit these values in
`config/DistantHorizons.toml`:

```toml
[common.multiThreading]
numberOfThreads = 4
threadRunTimeRatio = 0.50
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
