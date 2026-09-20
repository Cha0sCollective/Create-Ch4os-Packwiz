# Client installation

1. Install [Prism Launcher](https://prismlauncher.org/).
2. Choose **Add Instance → Import**. Select the [ZIP](https://github.com/Cha0sCollective/Create-Ch4os-Packwiz/releases/download/channel-public/Create-Ch4oS-Public-Prism.zip) or paste:

   ```text
   https://github.com/Cha0sCollective/Create-Ch4os-Packwiz/releases/download/channel-public/Create-Ch4oS-Public-Prism.zip
   ```

3. In **Settings → Java**, select Java 21 and set your memory. New imports use a 12 GiB maximum heap.
   Leave room for other applications; lower it on a 16 GiB PC if needed.
4. Sign in with Minecraft and launch. Allow the Packwiz pre-launch command when
   prompted. The first launch downloads the pack.

The instance inherits Prism's Java selection and supplies
its recommended Java 21 garbage-collector arguments. Large DH generation jobs
may need more memory. Existing instances keep their current memory setting;
set **Edit Instance → Settings → Java → Maximum memory** to **12288 MiB** to adopt it.

See [Maps and distant terrain](MAPS.md) for beta defaults and existing-instance settings.

## Updates and removal

The Public import follows `public`; the [Beta import](https://github.com/Cha0sCollective/Create-Ch4os-Packwiz/releases/tag/channel-beta)
follows `beta`. A numbered release ZIP stays on its tagged commit, even after
either branch advances. Download its attached Prism ZIP, not the source archive.
Each choice has a separate instance identity. Use a separate instance when
switching versions; do not downgrade an existing world.

The original public-following 0.2.0 ZIP is replaced by a fixed 0.2.0 download during
the release-process migration. Instances imported before that replacement still
follow public; replacing a download does not change their pre-launch commands.

Launching checks the selected pack URL. If a download fails, resolve the
reported problem and retry before playing. Extra mods you add are your responsibility.
Back up local worlds before updating; this pack does not migrate AOCA/RC8 saves.

Remove the instance through Prism after saving any worlds or schematics you want
to keep. Nothing needs uninstalling through Windows Apps.
