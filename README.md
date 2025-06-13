# mrcn-zmnsk-playground

A version-controlled, structured repository for mini projects, experiments, and proofs-of-concept designed for learning, exploration, and sharing with the community.

## Table of Contents

* [About](#about)
* [Repository Structure](#repository-structure)
* [Getting Started](#getting-started)
* Projects
  - [General AI Assistant benchmark Agent](hf-gaia/)
  - [LangGraph-ragagent](langgraph-ragagent/)
  - [HF-agent](hf-agent/readme.md)
  - [HF-multiagent](hf-multiagent/readme.md)
  - [llama-agentworkflow](llama-agentworkflow/)
  - [ado-bugtriage-assistant](ado-bugtriage-aiassistant/readme.md)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## About

This repository is a personal playground for building small-scale projects, experiments, and demos. Each subfolder contains a self-contained mini project geared toward learning a new concept, language feature, or tool. By keeping these projects here, I can:

* Track progress and revisit past experiments
* Share code samples and learning resources with others
* Collaborate and receive feedback on implementations

## Repository Structure

```
/                     # Root of the playground
├── project-1/        # e.g., `docker-tutorial`
│   ├── README.md     # Project-specific description and instructions
│   ├── src/          # Source code files
│   └── ...           # Configuration, data, scripts
├── project-2/        # e.g., `flask-api-demo`
│   ├── README.md
│   ├── app/
│   └── ...
├── notebooks/        # Jupyter notebooks for data exploration or tutorials
├── docs/             # Shared documentation or diagrams
└── README.md         # This file
```

* **project-*/*:** Each mini project lives in its own directory with its own README and structure.
* **notebooks/**: Exploratory analyses and interactive tutorials.
* **scripts/**: Common utility scripts used across multiple projects.
* **docs/**: Diagrams, markdown notes, and reference material.

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/mrcn-zmnsk/mrcn-zmnsk-playground.git
   cd mrcn-zmnsk-playground
   ```
2. **Explore a project**: Navigate into any `project-*` folder and follow its instructions in `README.md`.
3. **Open notebooks**: Launch `jupyter lab` or `jupyter notebook` and open files in the `notebooks/` directory.

## Contributing

Contributions and feedback are welcome!

1. **Fork** the repository
2. **Create a branch** (`git checkout -b feature/new-project`)
3. **Add your project** under a new folder (e.g., `project-xyz`), including a `README.md` with clear instructions
4. **Commit** your changes (`git commit -m "Add project-xyz demo"`)
5. **Push** to your fork (`git push origin feature/new-project`)
6. **Open a Pull Request**, describing your project and any setup steps

Please ensure your code follows consistent naming and directory conventions.

## License

This repository is licensed under the [MIT License](LICENSE).

## Contact

Created by **mrcn-zmnsk**. Feel free to reach out:

* GitHub: [mrcn-zmnsk](https://github.com/mrcn-zmnsk)

Happy coding! Feel free to explore, learn, and share. :)
