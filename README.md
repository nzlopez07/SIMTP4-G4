# SIMTP4-G4
Repositorio contenedor para el Trabajo Práctico 4 de Simulación UTN-FRC

## Ejecutar la aplicación (un solo comando)

Se proveen scripts para ejecutar la aplicación con una sola instrucción:

- Windows (PowerShell):

```powershell
./run.ps1
```

- Linux / macOS:

```bash
./run.sh
```

Ambos scripts crean un entorno virtual en `.venv` (si no existe), instalan las dependencias desde `documentacion/requirements.txt`, y arrancan la aplicación Flask.

Alternativamente, si ya configuraste el entorno, podés usar directamente:

```bash
python main.py
```

