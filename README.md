# 🖥️ Legacy VNC Screen Sharing on Ubuntu 24.04

> Enable traditional VNC screen sharing using **x11vnc** on Ubuntu 24.04 or Ubuntu-based distros (such as Winux) — even with Wayland as the default display server!

---

## 📖 Quick Tutorial: Enabling Traditional VNC Screen Sharing on Ubuntu 24.04

The following is an auto-generated tutorial (see `tutorial.py`) for setting up legacy VNC screen sharing with x11vnc:

### the step-by-step guide

**Step 1: Understand the Context**
- Ubuntu 24.04 uses Wayland as the default display server.
- x11vnc requires the legacy Xorg server to function.
- To enable classic VNC sharing of your real desktop screen, you must disable Wayland and use Xorg.

**Step 2: Disable Wayland and Switch to Xorg**
1. Open terminal.
2. Edit the GDM configuration:
   ```
   sudo nano /etc/gdm3/custom.conf
   ```
3. Find the line:
   ```
   #WaylandEnable=false
   ```
4. Uncomment it by removing the `#`:
   ```
   WaylandEnable=false
   ```
5. Save file (`Ctrl+O`, Enter) and exit (`Ctrl+X`).
6. Restart GDM to apply changes:
   ```
   sudo systemctl restart gdm3
   ```
   > Warning: This will close all open GUI applications and log you out.
7. Log in again.
8. Verify that Xorg is running instead of Wayland:
   ```
   echo $XDG_SESSION_TYPE
   ```
   You should see:
   ```
   x11
   ```

**Step 3: Install Necessary Fonts (Fixes VNC font errors)**
1. Update package lists:
   ```
   sudo apt update
   ```
2. Install common X fonts:
   ```
   sudo apt install xfonts-base xfonts-100dpi xfonts-75dpi xfonts-scalable
   ```

**Step 4: Install x11vnc**
```
sudo apt install x11vnc
```

**Step 5: Set VNC Password**
1. Run:
   ```
   x11vnc -storepasswd
   ```
2. Enter and confirm a password.
3. The password is saved at `~/.vnc/passwd`.

**Step 6: Start x11vnc Manually (Share your real desktop)**
Run:
```
x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth ~/.vnc/passwd -rfbport 5900 -shared -bg
```
**Explanation of important flags:**
- `-auth guess` : try to find correct Xauthority file automatically
- `-forever` : keep server running after clients disconnect
- `-loop` : restart if server crashes
- `-noxdamage` : fix some screen update issues
- `-repeat` : allow key repeats
- `-rfbauth ~/.vnc/passwd` : use the password file
- `-rfbport 5900` : listen on standard VNC port 5900
- `-shared` : allow multiple clients
- `-bg` : run in background

**Step 7: Connect with VNC Client**
- Use any VNC client (RealVNC, TigerVNC, TightVNC Viewer, Remmina, etc.)
- Connect to your Ubuntu machine IP on port 5900.
- Enter the VNC password you set earlier.

**Step 8 (Optional): Create a systemd Service to Auto-Start x11vnc on Boot**
1. Create a service file:
   ```
   sudo nano /etc/systemd/system/x11vnc.service
   ```
2. Paste this, replace `yourusername` with your Ubuntu username:
   ```
   [Unit]
   Description=Start x11vnc at startup
   After=graphical.target

   [Service]
   Type=simple
   User=yourusername
   ExecStart=/usr/bin/x11vnc -auth /home/yourusername/.Xauthority -forever -loop -noxdamage -repeat -rfbauth /home/yourusername/.vnc/passwd -rfbport 5900 -shared
   Restart=on-failure

   [Install]
   WantedBy=graphical.target
   ```
3. Save and exit.
4. Enable and start the service:
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable x11vnc.service
   sudo systemctl start x11vnc.service
   ```
5. Check service status:
   ```
   sudo systemctl status x11vnc.service
   ```

**Troubleshooting & Tips**
- If you get "XOpenDisplay failed", check if you are running Wayland (`echo $XDG_SESSION_TYPE`). You must switch to Xorg.
- Ensure you run x11vnc as the same user logged into the desktop.
- If VNC connection fails, verify firewall allows port 5900.
- Use `ps aux | grep x11vnc` to confirm the VNC server is running.
- If fonts appear broken on VNC clients, ensure fonts are installed.
- Restart your machine if you run into session or display auth issues.

**Notes**
- Restarting GDM or rebooting closes all open GUI apps.
- Connect to VNC on port 5900 using your favorite VNC client.
- Make sure firewall allows port 5900.



---

## 📦 Contents

- `tutorial.py` — Python script to generate the tutorial PDF.
- `x11vnc_legacy_vnc_tutorial_ubuntu_24_04.pdf` — The PDF guide created by `tutorial.py`.
- This README.

---

## 🚀 Features

- **Works on Ubuntu 24.04 & derivatives**
- **Handles Wayland-to-Xorg switch**
- **Covers x11vnc installation & configuration**
- **PDF tutorial generator for offline reference**
- **Systemd service setup for auto-start**
- **Troubleshooting & tips included**

---

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/gedeeinstein/legacy-vnc-ubuntu.git
cd legacy-vnc-ubuntu
```

### 2. Generate the PDF Tutorial

Make sure you have `fpdf` installed:

```bash
pip install fpdf
```

Run the script:

```bash
python3 tutorial.py
```

The PDF will be saved as `x11vnc_legacy_vnc_tutorial_ubuntu_24_04.pdf`.

---

## 💡 Why Use This?

- **Wayland Compatibility:** Ubuntu 24.04 defaults to Wayland, which breaks traditional VNC workflows—this guide fixes that.
- **Real Desktop Sharing:** Unlike virtual desktop servers, `x11vnc` shares your actual logged-in session.
- **Automation Ready:** The Python script means you always have a portable, printable reference.

---

## 🧑‍💻 Requirements

- Ubuntu 24.04 or derivative
- Python 3.x
- `fpdf` Python package

---

## 🔒 Security Note

- Always set a strong VNC password.
- Ensure your firewall settings allow port 5900 only from trusted networks.
- Consider tunneling VNC over SSH for extra security.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Pull requests, suggestions, and improvements are welcome!  
Open an issue or fork the repo to get started.

---

## 📬 Contact

Maintained by [gedeeinstein](https://github.com/gedeeinstein).  
Feel free to connect or ask questions!
