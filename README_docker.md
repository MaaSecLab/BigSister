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

To run the tool:

```bash
docker compose run --rm bigsister
```

### 4. GUI VS Terminal

When starting the application, you will be given two choices:

```bash
=== Big Sister - Metadata and Image Analysis Tool ===
Choose your interface:
1. GUI (Graphical User Interface)
2. Terminal (Command Line Interface)
Enter 1 or 2:
```

If you want to use **terminal option (1)**, you need to specify the file, like this:

```bash
docker compose run --rm bigsister /downloads/example_image.jpeg
```
