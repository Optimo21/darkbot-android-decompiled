#!/usr/bin/env python3
"""
Script para descargar, descomprimir y descompilar APK de Darkbot Android
Extrae todo con apktool y jadx, organiza en carpetas y lo sube a GitHub
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Configuración
APK_URL = "https://github.com/Optimo21/darkbot.-android/releases/download/01/darkorbit-v0.1.1-android.apk"
APK_NAME = "darkorbit-v0.1.1-android.apk"
WORK_DIR = Path.cwd()
ORIGINAL_DIR = WORK_DIR / "original"
DECOMPILED_DIR = WORK_DIR / "decompiled"

def run_command(cmd, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    if result.returncode != 0:
        print(f"⚠️  Advertencia en: {description}")
    return result.returncode == 0

def check_tools():
    """Verifica que apktool y jadx estén instalados"""
    print("\n🔍 Verificando herramientas necesarias...\n")
    
    tools = {
        "apktool": "apktool d --version",
        "jadx": "jadx --version",
        "git": "git --version",
    }
    
    missing = []
    for tool, cmd in tools.items():
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"✅ {tool}: instalado")
        else:
            print(f"❌ {tool}: NO encontrado")
            missing.append(tool)
    
    if missing:
        print(f"\n⚠️  Herramientas faltantes: {', '.join(missing)}")
        print("Instálalas antes de continuar")
        sys.exit(1)
    
    print("\n✅ Todas las herramientas disponibles\n")

def setup_directories():
    """Crea las carpetas necesarias"""
    print("\n📁 Creando estructura de directorios...\n")
    
    ORIGINAL_DIR.mkdir(exist_ok=True)
    DECOMPILED_DIR.mkdir(exist_ok=True)
    
    print(f"✅ {ORIGINAL_DIR}")
    print(f"✅ {DECOMPILED_DIR}")

def download_apk():
    """Descarga el APK desde GitHub"""
    apk_path = ORIGINAL_DIR / APK_NAME
    
    if apk_path.exists():
        print(f"\n✅ APK ya existe: {apk_path}")
        return True
    
    print(f"\n📥 Descargando APK desde GitHub...")
    run_command(
        f'curl -L "{APK_URL}" -o "{apk_path}"',
        "Descargando APK"
    )
    
    if apk_path.exists():
        size_mb = apk_path.stat().st_size / (1024 * 1024)
        print(f"✅ APK descargado: {size_mb:.2f} MB")
        
        # Calcular SHA256
        run_command(
            f'sha256sum "{apk_path}" > "{apk_path}.sha256"',
            "Calculando SHA256"
        )
        
        with open(f"{apk_path}.sha256", "r") as f:
            print(f"📊 Hash: {f.read().strip()}")
        
        return True
    else:
        print(f"❌ Error descargando APK")
        return False

def extract_with_apktool():
    """Extrae el APK con apktool"""
    apk_path = ORIGINAL_DIR / APK_NAME
    output_dir = DECOMPILED_DIR / "apktool_output"
    
    if output_dir.exists():
        print(f"\n✅ Extracción con apktool ya existe: {output_dir}")
        return True
    
    output_dir.mkdir(exist_ok=True)
    
    success = run_command(
        f'apktool d -f "{apk_path}" -o "{output_dir}"',
        "Extrayendo APK con apktool"
    )
    
    if success and output_dir.exists():
        print(f"✅ APK extraído en: {output_dir}")
        return True
    else:
        print(f"❌ Error extrayendo con apktool")
        return False

def decompile_with_jadx():
    """Descompila el APK con jadx"""
    apk_path = ORIGINAL_DIR / APK_NAME
    output_dir = DECOMPILED_DIR / "jadx_output"
    
    if output_dir.exists():
        print(f"\n✅ Descompilación con jadx ya existe: {output_dir}")
        return True
    
    output_dir.mkdir(exist_ok=True)
    
    success = run_command(
        f'jadx -d "{output_dir}" --no-res "{apk_path}"',
        "Descompilando APK con jadx"
    )
    
    if success and output_dir.exists():
        print(f"✅ APK descompilado en: {output_dir}")
        return True
    else:
        print(f"❌ Error descompilando con jadx")
        return False

def organize_output():
    """Organiza la salida en estructura legible"""
    print(f"\n📑 Organizando archivos...\n")
    
    apktool_dir = DECOMPILED_DIR / "apktool_output"
    jadx_dir = DECOMPILED_DIR / "jadx_output"
    
    # Copiar AndroidManifest.xml
    if (apktool_dir / "AndroidManifest.xml").exists():
        shutil.copy(
            apktool_dir / "AndroidManifest.xml",
            DECOMPILED_DIR / "AndroidManifest.xml"
        )
        print("✅ AndroidManifest.xml")
    
    # Copiar recursos
    if (apktool_dir / "res").exists():
        if (DECOMPILED_DIR / "res").exists():
            shutil.rmtree(DECOMPILED_DIR / "res")
        shutil.copytree(
            apktool_dir / "res",
            DECOMPILED_DIR / "res"
        )
        print("✅ Recursos (res/)")
    
    # Copiar assets
    if (apktool_dir / "assets").exists():
        if (DECOMPILED_DIR / "assets").exists():
            shutil.rmtree(DECOMPILED_DIR / "assets")
        shutil.copytree(
            apktool_dir / "assets",
            DECOMPILED_DIR / "assets"
        )
        print("✅ Assets (/assets)")
    
    # Copiar librerías
    if (apktool_dir / "lib").exists():
        if (DECOMPILED_DIR / "lib").exists():
            shutil.rmtree(DECOMPILED_DIR / "lib")
        shutil.copytree(
            apktool_dir / "lib",
            DECOMPILED_DIR / "lib"
        )
        print("✅ Librerías (lib/)")
    
    # Copiar código fuente descompilado
    if (jadx_dir / "sources").exists():
        if (DECOMPILED_DIR / "sources").exists():
            shutil.rmtree(DECOMPILED_DIR / "sources")
        shutil.copytree(
            jadx_dir / "sources",
            DECOMPILED_DIR / "sources"
        )
        print("✅ Código descompilado (sources/)")
    
    # Limpiar temporales
    if apktool_dir.exists():
        shutil.rmtree(apktool_dir)
    if jadx_dir.exists():
        shutil.rmtree(jadx_dir)
    
    print("\n✅ Archivos organizados")

def create_index():
    """Crea un archivo INDEX.md"""
    index_content = """# Índice de Contenido Descompilado

## 📱 APK: Darkbot Android v0.1.1

### 📁 Estructura

#### Código Fuente Descompilado
- **`/sources`** - Código Java/Kotlin descompilado
  - Todas las clases de la aplicación
  - Código legible y navegable
  - Busca aquí la lógica de la aplicación

#### Configuración
- **`AndroidManifest.xml`** - Archivo de manifiesto
  - Permisos requeridos
  - Actividades
  - Servicios
  - Receptores
  - Proveedores de contenido
  - Intenciones

#### Recursos
- **`/res`** - Recursos de la aplicación
  - `drawable/` - Imágenes, vectores
  - `layout/` - Layouts XML
  - `values/` - Strings, colores, estilos, dimensiones
  - `menu/` - Definiciones de menú
  - `anim/` - Animaciones

#### Assets
- **`/assets`** - Archivos de datos
  - Archivos incluidos en la APK
  - Datos estáticos de la aplicación

#### Librerías Nativas
- **`/lib`** - Librerías compiladas (.so)
  - Código compilado en C/C++
  - Funciones nativas de la aplicación

---

## 🔍 Cómo Navegar

1. **Buscar una clase**: Abre `/sources` y busca por nombre
2. **Ver permisos**: Abre `AndroidManifest.xml`
3. **Ver recursos**: Explora `/res`
4. **Ver configuración**: Abre `apktool.yml`

## 📊 Información

| Campo | Valor |
|-------|-------|
| Nombre APK | darkorbit-v0.1.1-android.apk |
| Versión | 0.1.1 |
| Herramienta Extracción | apktool 2.11.0 |
| Herramienta Descompilación | jadx 1.5.0 |
| Fecha | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |

---

✅ Todo el contenido está listo para revisar públicamente en GitHub
"""
    
    index_path = DECOMPILED_DIR / "INDEX.md"
    with open(index_path, "w") as f:
        f.write(index_content)
    
    print(f"✅ Índice creado: {index_path}")

def commit_and_push():
    """Hace commit y push a GitHub"""
    print(f"\n📤 Subiendo a GitHub...\n")
    
    os.chdir(WORK_DIR)
    
    run_command("git add -A", "Agregando archivos a git")
    run_command(
        f'git commit -m "🔄 APK descompilado completamente - {datetime.now().strftime(\'%Y-%m-%d %H:%M:%S\')}"',
        "Creando commit"
    )
    run_command("git push origin main", "Subiendo a GitHub")
    
    print("\n✅ Subido a GitHub correctamente")

def print_summary():
    """Imprime resumen final"""
    print(f"\n{'='*60}")
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print(f"{'='*60}\n")
    
    print("📊 Estructura generada:\n")
    
    for root, dirs, files in os.walk(DECOMPILED_DIR):
        level = root.replace(str(DECOMPILED_DIR), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}📁 {os.path.basename(root)}/')
        
        if level < 2:  # Limitar profundidad
            sub_indent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Mostrar primeros 5 archivos
                print(f'{sub_indent}📄 {file}')
            if len(files) > 5:
                print(f'{sub_indent}📄 ... +{len(files) - 5} archivos más')
    
    print(f"\n📍 Ubicación: {DECOMPILED_DIR}")
    print(f"🔗 Repositorio: https://github.com/Optimo21/darkbot-android-decompiled")
    print(f"⏰ Completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🚀 DESCOMPILADOR APK - DARKBOT ANDROID")
    print("="*60)
    
    check_tools()
    setup_directories()
    
    if not download_apk():
        sys.exit(1)
    
    if not extract_with_apktool():
        sys.exit(1)
    
    if not decompile_with_jadx():
        sys.exit(1)
    
    organize_output()
    create_index()
    commit_and_push()
    print_summary()

if __name__ == "__main__":
    main()
