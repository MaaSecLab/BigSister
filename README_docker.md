### 1. Prerequisites

Make sure you have Docker installed on your system.

- For Windows or macOS, get **Docker Desktop**.
- For Linux, follow the official **Docker Engine** installation guide.

> **Note on `sudo`**: The commands below assume you have completed the [official Docker post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) for Linux, which allow you to run Docker without `sudo`. If you get a `permission denied` error, you can either prefix the commands with `sudo` or follow that guide to add your user to the `docker` group.

### 2. First-Time Setup (Build the Image)

Before you can run the application, you need to build the Docker image. This command downloads all the dependencies and sets up the environment defined in the `Dockerfile`.

From the project's root directory (`~/BigSister`), run:

```bash
docker compose build
```

### 3. Running the Tool

To run the tool, you need to use this command:

```bash
docker compose run --rm bigsister
```

There are 2 different versions of the app (terminal and GUI), read instructions below.

#### Terminal App

When starting the application, you will be given two choices:

```bash
=== Big Sister - Metadata and Image Analysis Tool ===
Choose your interface:
1. GUI (Graphical User Interface)
2. Terminal (Command Line Interface)
Enter 1 or 2:
```

If you want to use **terminal option (2)**, you need to specify the file, like this:

```bash
docker compose run --rm bigsister /downloads/example_image.jpeg
```

#### GUI App

- **Linux**

  Before running the app, make sure to run:

  ```bash
  xhost +local:
  ```

  With this commad you are adding non-network local connections to your access control list. Without this command you will see `Authorization required, but no authorization protocol specified`.

  Then, you can run as usual:

  ```bash
  docker compose run --rm bigsister
  ```

- **Windows**

  Use [x11docker](https://github.com/mviereck/x11docker)

- **MacOS**

  Use [distrobox](https://github.com/89luca89/distrobox)

### 4. Get access to the files

By default Docker containers do not get access to the file system of the host.

In order to pass files to be analyzed, you need to map Docker volumes in the `docker-compose.yml`. We map current directory and `~/Downloads` by default:

```bash
volumes:
      # Map X11 file for GUI
      - /tmp/.X11-unix:/tmp/.X11-unix
      # Make current host directory available within container as /app
      - .:/app
      # Example for making other directories available
      - ~/Downloads:/Downloads
```

With this setup you can reference files, like this:

```bash
# A file in current directory
$ docker compose run --rm bigsister image.png
# Another file in host's ~/Downloads
$ docker compose run --rm bigsister /Downloads/another.png
```

You can add more directories by modifying `docker-compose.yml`
