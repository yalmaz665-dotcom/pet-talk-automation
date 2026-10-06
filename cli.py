#!/usr/bin/env python3
"""
Pet Talk Automation CLI
Komut satırından tam sistem yönetimi
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

class PetTalkCLI:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / ".venv"
        self.env_file = self.project_dir / ".env"
        self.output_dir = self.project_dir / "videos" / "output"
        self.data_dir = self.project_dir / "data"
        
    def setup(self):
        """Sistemi kur ve hazırla"""
        print("🚀 Pet Talk Automation Kurulumu Başlatılıyor...\n")
        
        # Git pull
        print("📥 Son değişiklikler alınıyor...")
        subprocess.run(["git", "pull", "origin", "main"], cwd=self.project_dir)
        
        # Pillow versiyonunu düzelt
        print("🔧 requirements.txt düzeltiliyor...")
        req_file = self.project_dir / "requirements.txt"
        content = req_file.read_text()
        content = content.replace("Pillow==11.1.0", "Pillow==10.1.0")
        req_file.write_text(content)
        
        # Venv oluştur
        if not self.venv_dir.exists():
            print("🐍 Sanal ortam oluşturuluyor...")
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)])
        
        # Paketleri yükle
        print("📦 Paketler yükleniyor...")
        pip_exe = self.venv_dir / "bin" / "pip"
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip", "setuptools", "wheel"])
        subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], cwd=self.project_dir)
        
        # .env oluştur
        if not self.env_file.exists():
            print("⚙️ .env dosyası oluşturuluyor...")
            env_example = self.project_dir / ".env.example"
            self.env_file.write_text(env_example.read_text())
        
        # Dizinleri oluştur
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ Kurulum tamamlandı!\n")
    
    def run(self):
        """Video oluştur ve YouTube'a yükle"""
        print("\n╔════════════════════════════════════════╗")
        print("║     🎬 Pet Talk Automation System      ║")
        print(f"║           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}           ║")
        print("╚════════════════════════════════════════╝\n")
        
        # Kontrol
        if not self.env_file.exists():
            print("❌ .env dosyası bulunamadı!")
            print("   Lütfen önce 'python cli.py setup' çalıştırın")
            sys.exit(1)
        
        env_content = self.env_file.read_text()
        if not any(key in env_content for key in ["ANTHROPIC_API_KEY=", "ELEVENLABS_API_KEY="]):
            print("⚠️ UYARI: .env dosyasında API anahtarları boş görünüyor!")
            print("   Lütfen .env dosyasını doldurun:\n")
            print("   - ANTHROPIC_API_KEY: Claude API anahtarı")
            print("   - ELEVENLABS_API_KEY: ElevenLabs API anahtarı")
            print("   - YOUTUBE_CLIENT_ID ve SECRET: YouTube OAuth\n")
        
        os.chdir(self.project_dir)
        sys.path.insert(0, str(self.project_dir))
        
        try:
            print("🎥 Video oluşturuluyor...\n")
            from src.main import main
            main()
            
            # Son video dosyasını bul
            videos = sorted(self.output_dir.glob("*.mp4"), key=os.path.getmtime, reverse=True)
            if videos:
                latest = videos[0]
                size = latest.stat().st_size / (1024 * 1024)  # MB
                print(f"\n✅ Video başarıyla oluşturuldu!")
                print(f"📁 Konum: {latest}")
                print(f"📊 Boyut: {size:.2f} MB")
                print(f"⏱️  Oluşturma zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\n🎉 Sistem başarıyla tamamlandı!")
                return 0
            else:
                print("\n❌ Video oluşturulamadı!")
                return 1
                
        except Exception as e:
            print(f"\n❌ Hata oluştu: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    def status(self):
        """Sistem durumunu kontrol et"""
        print("\n📊 Sistem Durumu:\n")
        
        checks = [
            ("Sanal ortam", self.venv_dir.exists()),
            (".env dosyası", self.env_file.exists()),
            ("Videos dizini", self.output_dir.exists()),
            ("Data dizini", self.data_dir.exists()),
        ]
        
        for name, exists in checks:
            status = "✅" if exists else "❌"
            print(f"  {status} {name}")
        
        # Son videolar
        if self.output_dir.exists():
            videos = sorted(self.output_dir.glob("*.mp4"), key=os.path.getmtime, reverse=True)
            if videos:
                print(f"\n📹 Son videolar ({len(videos)}):")
                for video in videos[:5]:
                    size = video.stat().st_size / (1024 * 1024)
                    mtime = datetime.fromtimestamp(video.stat().st_mtime)
                    print(f"     • {video.name} ({size:.2f} MB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print()
    
    def clean(self):
        """Geçici dosyaları temizle"""
        print("\n🧹 Geçici dosyalar temizleniyor...\n")
        
        import shutil
        
        # __pycache__ dizinlerini sil
        for root, dirs, files in os.walk(self.project_dir):
            if "__pycache__" in dirs:
                pycache = os.path.join(root, "__pycache__")
                shutil.rmtree(pycache)
                print(f"  🗑️ Silindi: {pycache}")
        
        print("\n✅ Temizlik tamamlandı!")
    
    def logs(self):
        """Son günlükleri göster"""
        print("\n📋 Son Günlükler:\n")
        
        # Veritabanından son kayıtları oku
        db_path = self.data_dir / "videos.db"
        if db_path.exists():
            try:
                import sqlite3
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT date, title, status, created_at FROM videos ORDER BY created_at DESC LIMIT 10")
                
                print(f"{'Tarih':<12} {'Durum':<10} {'Başlık':<40}")
                print("-" * 62)
                
                for date, title, status, created_at in cursor.fetchall():
                    status_icon = "✅" if status == "uploaded" else "⏳"
                    title_short = (title[:37] + "...") if len(title) > 40 else title
                    print(f"{date:<12} {status_icon} {status:<8} {title_short:<40}")
                
                conn.close()
            except Exception as e:
                print(f"❌ Hata: {e}")
        else:
            print("   Henüz video oluşturulmadı.")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Pet Talk Automation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python cli.py setup        - Sistemi kur ve hazırla
  python cli.py run          - Video oluştur ve yükle
  python cli.py status       - Sistem durumunu kontrol et
  python cli.py clean        - Geçici dosyaları temizle
  python cli.py logs         - Son günlükleri göster
        """)
    
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=["setup", "run", "status", "clean", "logs"],
        help="Çalıştırılacak komut (default: run)"
    )
    
    args = parser.parse_args()
    
    cli = PetTalkCLI()
    
    if args.command == "setup":
        cli.setup()
    elif args.command == "run":
        sys.exit(cli.run())
    elif args.command == "status":
        cli.status()
    elif args.command == "clean":
        cli.clean()
    elif args.command == "logs":
        cli.logs()


if __name__ == "__main__":
    main()
