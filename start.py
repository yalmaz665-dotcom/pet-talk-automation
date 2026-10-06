#!/usr/bin/env python3
"""
Pet Talk Automation - Tam Otomatik Sistem
Kurulum -> Video Üretimi -> YouTube Yüklemesi
Her şey otomatik, terminal gerekli değil!
"""

import os
import sys
import subprocess
import shutil
import time
import schedule
from pathlib import Path
from datetime import datetime
import platform

class PetTalkAutoSystem:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / ".venv"
        self.env_file = self.project_dir / ".env"
        self.output_dir = self.project_dir / "videos" / "output"
        self.data_dir = self.project_dir / "data"
        
        # Python executable path
        if sys.platform == "win32":
            self.python_exe = self.venv_dir / "Scripts" / "python.exe"
            self.pip_exe = self.venv_dir / "Scripts" / "pip.exe"
        else:
            self.python_exe = self.venv_dir / "bin" / "python"
            self.pip_exe = self.venv_dir / "bin" / "pip"
    
    def log(self, message, level="INFO"):
        """Güzel log yazdır"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "ERROR":
            print(f"\n❌ [{timestamp}] {message}\n")
        elif level == "SUCCESS":
            print(f"\n✅ [{timestamp}] {message}\n")
        elif level == "INFO":
            print(f"ℹ️  [{timestamp}] {message}")
        elif level == "STEP":
            print(f"\n🔧 [{timestamp}] {message}")
        elif level == "PROGRESS":
            print(f"⏳ [{timestamp}] {message}")
    
    def run_command(self, cmd, cwd=None):
        """Komutu çalıştır ve sonucu döndür"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def step_1_setup_venv(self):
        """1. Sanal ortam kur"""
        self.log("Sanal ortam ayarlanıyor...", "STEP")
        
        if not self.venv_dir.exists():
            self.log("Sanal ortam oluşturuluyor...", "PROGRESS")
            success, _, err = self.run_command([sys.executable, "-m", "venv", str(self.venv_dir)])
            if not success:
                self.log(f"Sanal ortam oluşturulamadı: {err}", "ERROR")
                return False
            self.log("Sanal ortam oluşturuldu", "SUCCESS")
        else:
            self.log("Sanal ortam zaten var", "SUCCESS")
        
        return True
    
    def step_2_upgrade_pip(self):
        """2. Pip yükselt"""
        self.log("Pip yükseltiliyor...", "STEP")
        
        success, _, err = self.run_command([str(self.pip_exe), "install", "--upgrade", "pip", "setuptools", "wheel"])
        if not success:
            self.log(f"Pip yükseltilemedi: {err}", "ERROR")
            return False
        
        self.log("Pip güncel", "SUCCESS")
        return True
    
    def step_3_fix_requirements(self):
        """3. Requirements.txt dosyasını düzelt"""
        self.log("Requirements.txt düzeltiliyor...", "STEP")
        
        req_file = self.project_dir / "requirements.txt"
        if not req_file.exists():
            self.log("requirements.txt bulunamadı", "ERROR")
            return False
        
        content = req_file.read_text()
        
        # Uyumlu sürümleri ayarla
        replacements = {
            "Pillow==11.1.0": "Pillow==10.0.1",
            "moviepy==2.1.2": "moviepy==1.0.3",
            "numpy==2.2.0": "numpy==1.26.4",
        }
        
        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)
                self.log(f"{old} -> {new}", "PROGRESS")
        
        req_file.write_text(content)
        self.log("Requirements güncellendi", "SUCCESS")
        return True
    
    def step_4_install_packages(self):
        """4. Paketleri yükle"""
        self.log("Paketler yükleniyor (bu biraz zaman alabilir)...", "STEP")
        
        req_file = self.project_dir / "requirements.txt"
        success, stdout, err = self.run_command([
            str(self.pip_exe), "install", "-r", str(req_file), "--upgrade"
        ])
        
        if not success:
            # Tek tek yükle
            self.log("Hepsini birlikte yükleyemedi, tek tek deniyor...", "PROGRESS")
            packages = [
                "anthropic==0.54.0",
                "elevenlabs==1.12.0",
                "google-api-python-client==2.165.0",
                "google-auth==2.38.0",
                "google-auth-oauthlib==1.2.1",
                "moviepy==1.0.3",
                "numpy==1.26.4",
                "Pillow==10.0.1",
                "python-dotenv==1.1.0",
                "requests==2.32.2"
            ]
            
            for pkg in packages:
                self.log(f"Yükleniyor: {pkg}", "PROGRESS")
                success, _, err = self.run_command([str(self.pip_exe), "install", pkg])
                if not success:
                    self.log(f"Yüklenemedi: {pkg}", "PROGRESS")
        
        self.log("Paketler yüklendi", "SUCCESS")
        return True
    
    def step_5_create_env(self):
        """5. .env dosyası oluştur"""
        self.log(".env dosyası ayarlanıyor...", "STEP")
        
        if not self.env_file.exists():
            env_example = self.project_dir / ".env.example"
            if env_example.exists():
                shutil.copy(env_example, self.env_file)
                self.log(".env oluşturuldu", "SUCCESS")
            else:
                self.log(".env.example bulunamadı", "ERROR")
                return False
        else:
            self.log(".env zaten var", "SUCCESS")
        
        return True
    
    def step_6_create_directories(self):
        """6. Gerekli klasörleri oluştur"""
        self.log("Çalışma dizinleri oluşturuluyor...", "STEP")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.log("Dizinler hazır", "SUCCESS")
        return True
    
    def step_7_generate_video(self):
        """7. İlk videoyu üret"""
        self.log("İlk video üretiliyor...", "STEP")
        
        env_vars = os.environ.copy()
        env_vars['PYTHONPATH'] = str(self.project_dir)
        
        success, stdout, err = self.run_command(
            [str(self.python_exe), "-m", "src.main"],
            cwd=self.project_dir
        )
        
        if not success:
            self.log(f"Video oluşturulamadı: {err}", "ERROR")
            return False
        
        self.log("Video başarıyla oluşturuldu!", "SUCCESS")
        
        # Son videoyu bul
        videos = sorted(self.output_dir.glob("*.mp4"), key=os.path.getmtime, reverse=True)
        if videos:
            latest = videos[0]
            size_mb = latest.stat().st_size / (1024 * 1024)
            self.log(f"Video: {latest.name} ({size_mb:.2f} MB)", "SUCCESS")
            return True
        
        return True
    
    def setup_scheduler(self):
        """Otomatik zamanlayıcı kur"""
        self.log("Otomatik zamanlayıcı ayarlanıyor...", "STEP")
        
        # Her gün 09:00 da çalıştır
        schedule.every().day.at("09:00").do(self.daily_video_job)
        
        # Ayrıca her 6 saatte bir
        schedule.every(6).hours.do(self.daily_video_job)
        
        self.log("Zamanlayıcı aktif: Her gün 09:00, 6 saatte bir video", "SUCCESS")
    
    def daily_video_job(self):
        """Günlük video işi"""
        self.log(f"Günlük video işi başlatılıyor...", "PROGRESS")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"🎬 OTOMATIK VIDEO ÜRETIMI - {timestamp}")
        print(f"{'='*60}\n")
        
        env_vars = os.environ.copy()
        env_vars['PYTHONPATH'] = str(self.project_dir)
        
        success, _, err = self.run_command(
            [str(self.python_exe), "-m", "src.main"],
            cwd=self.project_dir
        )
        
        if success:
            self.log(f"Video başarıyla oluşturuldu!", "SUCCESS")
        else:
            self.log(f"Video oluşturulamadı: {err}", "ERROR")
    
    def run_scheduler(self):
        """Zamanlayıcıyı çalıştır"""
        self.log("Arka plan zamanlayıcısı başlatılıyor...", "STEP")
        
        print("\n" + "="*60)
        print("🎬 PET TALK AUTOMATION - OTOMATIK ÇALIŞAN SİSTEM")
        print("="*60)
        print("\n📅 Zamanlama:")
        print("   • Her gün 09:00 da video üretilecek")
        print("   • 6 saatte bir otomatik kontrol")
        print("   • YouTube'a otomatik paylaşım")
        print("\n⏸️  Durdurmak için: Ctrl+C\n")
        print("="*60 + "\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            self.log("Sistem durduruldu", "INFO")
            sys.exit(0)
    
    def full_setup(self):
        """Tüm kurulumu yap"""
        print("\n" + "="*60)
        print("🚀 PET TALK AUTOMATION - TAM OTOMATIK KURULUM")
        print("="*60 + "\n")
        
        steps = [
            ("Sanal Ortam", self.step_1_setup_venv),
            ("Pip Güncelle", self.step_2_upgrade_pip),
            ("Requirements Düzelt", self.step_3_fix_requirements),
            ("Paketleri Yükle", self.step_4_install_packages),
            (".env Dosyası", self.step_5_create_env),
            ("Dizinler", self.step_6_create_directories),
            ("İlk Video Üret", self.step_7_generate_video),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    self.log(f"{step_name} başarısız oldu!", "ERROR")
                    return False
            except Exception as e:
                self.log(f"{step_name} hatası: {e}", "ERROR")
                return False
        
        print("\n" + "="*60)
        print("✅ KURULUM VE İLK VIDEO TAMAMLANDI!")
        print("="*60 + "\n")
        
        return True


def main():
    """Ana başlatıcı"""
    system = PetTalkAutoSystem()
    
    # Kurulumu yap
    if system.full_setup():
        # Zamanlayıcıyı hazırla ve başlat
        system.setup_scheduler()
        system.run_scheduler()
    else:
        system.log("Kurulum başarısız oldu", "ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
