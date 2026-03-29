# [GÜNCELLEME 5 - v2]: Crash-Safe Refactor
# - Tüm open()/close() çağrıları with open() ile değiştirildi.
#   Hata olsa da olmasa da dosya her durumda otomatik kapanır.
# - write_entry() içine atomik yazma eklendi: önce diary.tmp'ye yaz,
#   sonra os.replace() ile taşı. Dosya asla yarım/bozuk kalmaz.
# - Tüm fonksiyonlar try-except ile sarıldı.
#   Kullanıcı çökme yerine anlaşılır hata mesajı görür.
#-------------------------------------------------------------------------------------------

# [GÜNCELLEME 2 - v0]: Akıllı Kayıt Sistemi
# - Döngü/Liste kullanmadan (No-Loop) otomatik ID sayma ve dinamik tarih damgası eklendi.
# - 'encoding="utf-8"' ve '.replace("\n", " ")' ile veri güvenliği sağlandı.

# [GÜNCELLEME 3 - v1]: Yinelemeli Listeleme
# - 'for line in f' döngüsü ile tüm kayıtları satır satır okuma özelliği eklendi.
# - '.split("|")' yöntemiyle ID, Tarih ve Mesaj ayrıştırılarak tablo formatında sunuldu.

# [GÜNCELLEME 4 - v1]: Anahtar Kelime Arama
# - Tüm günlük içeriğinde kelime bazlı tarama (Keyword Search) motoru kuruldu.
# - '.lower()' metodu ile büyük/küçük harf duyarsız, esnek arama desteği sağlandı.

# [GÜNCELLEME 5 - v2]: Crash-Safe Refactor
# - Tüm 'open()'/'close()' çağrıları 'with open()' (Context Manager) ile değiştirildi.
#   Bu sayede program çökmesi veya bir hata oluşması durumunda dosya otomatik kapanır.
# - Tüm dosya I/O işlemleri 'try-except' blokları ile sarıldı.
#   'FileNotFoundError', 'PermissionError' ve genel 'OSError' ayrı ayrı yakalanır.
# - 'write_entry' içine atomik yazma (temp file + rename) eklendi.
#   Yazma yarıda kesilse bile mevcut 'diary.dat' hiçbir zaman bozulmaz.

"""
Mini-Diary v2.0 — Crash-Safe Implementation
Developer: Kadir Enes (Samsun University)
Features: init, write (v0) | list, search (v1) | context managers + exception handling (v2)
"""
import sys
import os
import time

DIARY_DIR  = ".minidiary"
DIARY_FILE = os.path.join(DIARY_DIR, "diary.dat")
DIARY_TMP  = os.path.join(DIARY_DIR, "diary.tmp")  # Atomik yazma için geçici dosya


def initialize():
    """Gizli klasör ve boş günlük dosyası oluşturur."""
    if os.path.exists(DIARY_DIR):
        return "[!] Already initialized."

    try:
        os.mkdir(DIARY_DIR)
        # 'with' bloğu: oluşturma başarısız olsa bile hiçbir kaynak sızıntısı olmaz.
        with open(DIARY_FILE, "w", encoding="utf-8"):
            pass  # Sadece boş dosyayı oluşturmak yeterli; yazacak içerik yok.
        return "[+] Initialized empty diary in .minidiary/"

    except PermissionError:
        # Kullanıcının bu dizinde klasör/dosya oluşturma yetkisi yoksa.
        return "[❌] Error: Permission denied. Cannot create diary directory."
    except OSError as e:
        # Disk dolu, geçersiz yol vb. diğer işletim sistemi hataları.
        return f"[❌] Error: Could not initialize diary. Details: {e}"


def write_entry(content):
    """
    Yeni bir yazı ekler. (v0 Logic: No loops/lists)

    Atomik Yazma Stratejisi:
      1. Yeni satırı önce geçici bir dosyaya (diary.tmp) yaz.
      2. Ardından os.replace() ile diary.tmp → diary.dat olarak yeniden adlandır.
      os.replace() işletim sistemi düzeyinde atomik olduğundan, program tam bu
      noktada çökse bile ya tam eski veri ya da tam yeni veri korunur; asla
      yarım/bozuk bir dosya oluşmaz.
    """
    if not os.path.exists(DIARY_FILE):
        return "[❌] Error: Initialize first using 'init'"

    try:
        # --- Adım 1: Mevcut içeriği oku ve yeni ID'yi hesapla ---
        with open(DIARY_FILE, "r", encoding="utf-8") as f:
            full_text = f.read()

        entry_id  = full_text.count("\n") + 1
        date_str  = time.strftime("%Y-%m-%d")
        clean_msg = content.replace("\n", " ")
        new_line  = f"{entry_id}|{date_str}|{clean_msg}\n"

        # --- Adım 2: Mevcut içerik + yeni satırı geçici dosyaya yaz ---
        # 'with' bloğu: istisna fırlatılsa bile geçici dosya düzgünce kapatılır.
        with open(DIARY_TMP, "w", encoding="utf-8") as tmp:
            tmp.write(full_text)  # Eski kayıtlar
            tmp.write(new_line)   # Yeni kayıt

        # --- Adım 3: Geçici dosyayı asıl dosyanın üzerine atomik olarak taşı ---
        # Bu satırdan önce program çökerse diary.dat sağlam kalır.
        # Bu satırdan sonra program çökerse yeni veri zaten diary.dat'a yazılmıştır.
        os.replace(DIARY_TMP, DIARY_FILE)

        return f"[✅] Entry saved with ID: {entry_id}"

    except FileNotFoundError:
        return "[❌] Error: Diary file not found. Please run 'init' first."
    except PermissionError:
        return "[❌] Error: Permission denied. Cannot write to diary file."
    except OSError as e:
        # Disk dolu veya geçici dosya taşıma başarısız gibi durumlar.
        return f"[❌] Error: Failed to save entry. Details: {e}"


def list_entries():
    """Tüm günlüğü listeler. (v1 Logic: Using For-Loop)"""
    if not os.path.exists(DIARY_FILE):
        return "[❌] Diary is empty or not initialized."

    try:
        print("\n" + "=" * 30)
        print("      YOUR DIARY LOGS")
        print("=" * 30)

        # 'with' bloğu: döngü sırasında hata olsa bile f.close() garantilenir.
        with open(DIARY_FILE, "r", encoding="utf-8") as f:
            has_entries = False
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    print(f"[{parts[0]}] {parts[1]} >> {parts[2]}")
                    has_entries = True

        if not has_entries:
            print("  (No entries yet. Use 'write' to add one.)")

        return "=" * 30

    except PermissionError:
        return "[❌] Error: Permission denied. Cannot read diary file."
    except OSError as e:
        return f"[❌] Error: Failed to read diary. Details: {e}"


def search_entries(keyword):
    """İçerikte arama yapar. (v1 Logic: Using For-Loop)"""
    if not os.path.exists(DIARY_FILE):
        return "[❌] Diary is empty or not initialized."

    print(f"\n[🔍] Searching for: '{keyword}'...")

    try:
        found = False

        # 'with' bloğu: arama sırasında hata olsa bile f.close() garantilenir.
        with open(DIARY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if keyword.lower() in line.lower():
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        print(f"-> Found in ID [{parts[0]}]: {parts[2]}")
                        found = True

        if not found:
            return "[!] No matches found."
        return "[✔] Search complete."

    except PermissionError:
        return "[❌] Error: Permission denied. Cannot read diary file."
    except OSError as e:
        return f"[❌] Error: Failed to search diary. Details: {e}"


# --- Ana Program (CLI Manager) ---

if len(sys.argv) < 2:
    print("\n--- Mini-Diary CLI v2.0 (Crash-Safe) ---")
    print("Commands: init | write \"msg\" | list | search \"keyword\"")

elif sys.argv[1] == "init":
    print(initialize())

elif sys.argv[1] == "write":
    if len(sys.argv) < 3:
        print("Usage: python solution.py write \"Your message\"")
    else:
        print(write_entry(sys.argv[2]))

elif sys.argv[1] == "list":
    print(list_entries())

elif sys.argv[1] == "search":
    if len(sys.argv) < 3:
        print("Usage: python solution.py search \"keyword\"")
    else:
        print(search_entries(sys.argv[2]))

else:
    print(f"[!] Unknown command: '{sys.argv[1]}'")
    print("    Valid commands: init | write | list | search")

