🚌 Public Transport Management System

Universidade Federal de Minas Gerais (UFMG) School of Engineering - Systems
Engineering Object-Oriented Programming - Project 1 (2026)

📖 About the Project

This project implements a pipeline to manage operational information for
a Public Transport System. It is divided into two main areas:

1.  Data Ingestion: Receives and processes operational data (latitude,
    longitude, demand, bus lines, point type) via a graphical user interface. It
    applies security validations (prevention against command injection and
    flood) and sanitizes data before local persistence.
2.  Data Administration & Management: Offers a control panel with authentication
    (password hashing) for tabular visualization and filtered export of records
    to .csv or .json formats.

🛠️ Technologies & Architecture

  - Language: Python
  - GUI Framework: Custontkinter
  - Data Storage: Local JSON and CSV files
  - Architecture Pattern: MVVM (Model-View-ViewModel)
  - Design Patterns: Dependency Injection

🧩 Object-Oriented Programming (OOP) Concepts Applied

The project's architecture is organized into logical layers, strictly following
the Single Responsibility Principle (SRP) and Don't Repeat Yourself (DRY).


1. Classes & Layers

  - Domain: The Ponto class is the main entity, encapsulating state (strictly
    private attributes) and formatting rules, accessed via getters and setters.
  - Use Cases/Logic: The ProcessadorDados class centralizes business rules,
    including data validation and security logic.
  - Infrastructure: Classes like GerenciadorJsonDados and
    GerenciadorAutenticacao handle I/O operations (file read/write) and
    cryptography.
  - Orchestration: The MainIntegrador class acts as an integration component,
    serving as a container for dependency injection.

2. Inheritance

  - Presentation Logic: InputViewModel and ResultadoViewModel inherit from the
    base class ViewModel.
  - Error Handling: The ExcecaoValidacaoSeguranca class inherits from Python's
    native Exception, allowing the system to throw and catch security errors
    clearly and semantically.

3. Polymorphism

Data repository injection is a central point. Since InputViewModel and
ResultadoViewModel derive from ViewModel, they share the same initialization
definition for the #repositorio: GerenciadorJsonDados attribute. The
MainIntegrador injects the same repository instance into different ViewModels,
ensuring uniform data access regardless of the active screen.

4. Abstract Classes

The ViewModel is an abstract class (<<abstract>>) that cannot be instantiated
directly. Its main function is to act as a "base contract" and manage shared
state (the JSON data repository) for its concrete subclasses, avoiding
redundancy in dependency injection.

👥 Team & Responsibilities

This project was developed collaboratively. Below is the breakdown of
implementations:

| Developer                               | Responsibilities / Classes Implemented                                   |
| :-------------------------------------- | :----------------------------------------------------------------------- |
| **Arthur Rafael Silva Teixeira**        | `TelaEntrada`, `InputViewModel`, `MainIntegrador`, `EstadosTelaEntrada`  |
| **Rafael Campello Soares**              | `TelaResultado`, `ResultadoViewModel`, `EstadosTelaEntrada`, `ViewModel` |
| **Gabriel Carvalho Pires**              | `Ponto`, `ProcessadorDados`, `GerenciadorAutenticacao`                   |
| **Gabriel Rodrigues Coutinho Mendonça** | `GerenciadorJsonDados`, Database Management (CSV/JSON)                   |

Belo Horizonte, 2026

## Dependencies

The SouBus project primarily uses Python's standard library. The following external libraries are required for graph visualization and the graphical interface:

```bash
pip install customtkinter matplotlib networkx
```

### Required Packages

- `customtkinter` — Modern graphical user interface.
- `matplotlib` — Graph plotting and visualization.
- `networkx` — Graph creation and manipulation.

### Using a Virtual Environment

It is recommended to create a virtual environment before installing dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Installing Dependencies Manually

If you are not using `requirements.txt`:

```bash
pip install customtkinter matplotlib networkx
sudo apt install python3-tk
```