#!/usr/bin/env python3
"""
Pet Talk Automation - Tam Otomatik Sistem
Kurulum, video üretimi, YouTube paylaşımı - Hepsi otomatik
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class AutoSetup:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / ".venv"
        
    def setup_environment(self):
        """Ortamı otomatik kur"""
        print("\n🚀 PET TALK AUTOMATION - OTOMATIK KURULUM\n")
        print("=" * 50)
        
        # 1. Python versiyonunu kontrol et
        print("\n1️⃣  Python versiyonu kontrol ediliyor...")
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"   {result.stdout.strip()}")
        
        # 2. Sanal ortam oluştur
        print("\n2️⃣  Sanal ortam oluşturuluyor...")
        if not self.venv_dir.exists():
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)])
            print(f"   ✅ {self.venv_dir}")
        else:
            print(f"   ✅ Zaten var: {self.venv_dir}")
        
        # 3. Pip upgrade
        print("\n3️⃣  Pip yükseltiliyor...")
        pip_path = self.venv_dir / ("Scripts" if sys.platform == "win32" else "bin") / "pip"
        subprocess.run([str(pip_path), "install", "--upgrade", "pip", "setuptools", "wheel"])
        print("   ✅ Pip güncel")
        
        # 4. Requirements.txt düzelt
        print("\n4️⃣  Requirements düzeltiliyor...")
        req_file = self.project_dir / "requirements.txt"
        content = req_file.read_text()
        # Pillow sürümünü uyumlu hale getir
        if "Pillow==11.1.0" in content:
            content = content.replace("Pillow==11.1.0", "Pillow==10.1.0")
        if "moviepy==2.1.2" in content:
            content = content.replace("moviepy==2.1.2", "moviepy==1.0.3")
        req_file.write_text(content)
        print("   ✅ Requirements güncellendi")
        
        # 5. Paketleri yükle
        print("\n5️⃣  Paketler yükleniyor (bu biraz zaman alabilir)...")
        subprocess.run([str(pip_path), "install", "-r", str(req_file)], cwd=self.project_dir)
        print("   ✅ Paketler kuruldu")
        
        # 6. .env oluştur
        print("\n6️⃣  Konfigürasyon dosyası oluşturuluyor...")
        env_file = self.project_dir / ".env"
        if not env_file.exists():
            env_example = self.project_dir / ".env.example"
            shutil.copy(env_example, env_file)
            print(f"   ✅ {env_file} oluşturuldu")
        else:
            print(f"   ✅ Zaten var: {env_file}")
        
        # 7. Klasörleri oluştur
        print("\n7️⃣  Çalışma dizinleri oluşturuluyor...")
        (self.project_dir / "videos" / "output").mkdir(parents=True, exist_ok=True)
        (self.project_dir / "data").mkdir(parents=True, exist_ok=True)
        print("   ✅ Dizinler hazır")
        
        print("\n" + "=" * 50)
        print("✅ KURULUM TAMAMLANDI!\n")
        
        return True

if __name__ == "__main__":
    setup = AutoSetup()
    setup.setup_environment()
    print("📝 Sonraki adım: 'python auto_run.py' komutunu çalıştır\n")
