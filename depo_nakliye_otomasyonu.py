# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 07:46:08 2026

@author: user
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyodbc
import time
import random


def get_db_connection():
    try:
        conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\MSSQLLocalDB;'
    'DATABASE=DepoNakliyeDB;'
    'Trusted_Connection=yes;'
)
        return conn
    except Exception as e:
        
        print("HATA DETAYI :")
        print (e)
        return None
    

class DepomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DEPOM - Depo Nakliye Otomasyonu")
        self.root.geometry("950x750")
        
        # Tema 
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TNotebook.Tab", padding=[15, 5], font=('Segoe UI', 10, 'bold'))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Sekmeler
        self.tab_depo = ttk.Frame(self.notebook)
        self.tab_lojistik = ttk.Frame(self.notebook)
        self.tab_satin_alma = ttk.Frame(self.notebook)
        self.tab_personeller = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_depo, text='   DEPO   ')
        self.notebook.add(self.tab_lojistik, text='  LOJİSTİK  ')
        self.notebook.add(self.tab_satin_alma, text=' SATIN ALMA ')
        self.notebook.add(self.tab_personeller, text='PERSONELLERİMİZ')

        self.sepet = []
        self.siparis_kodu = random.randint(10000, 99999)
        
        self.setup_depo()
        self.setup_lojistik()
        self.setup_satin_alma()
        self.setup_personel()

    # ---  DEPO BÖLÜMÜ ---
    def setup_depo(self):
        frame = tk.Frame(self.tab_depo, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="DEPO YÖNETİMİ", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Button(frame, text="Giriş Yap", width=25, height=2, bg="#2980b9", fg="white", font='bold',
                  command=lambda: self.login_window("emineberratunc", "ebt123", self.show_depo_sorgu)).pack(pady=10)
        tk.Button(frame, text="Göz At", width=25, height=2, bg="#27ae60", fg="white", font='bold',
                  command=self.depo_goz_at).pack(pady=10)

    def depo_goz_at(self):
        lbl = tk.Label(self.tab_depo, text="HOŞGELDİNİZ", font=("Segoe UI", 35, "bold"), fg="#2c3e50")
        lbl.place(relx=0.5, rely=0.4, anchor='center')
        self.root.update()
        time.sleep(5)
        lbl.destroy()
        self.show_veri_tablosu("Hızlı Bakış - Stok Listesi", "SELECT MalzemeAdi, StokAdet, Birim FROM dbo.Malzemeler")

    def show_depo_sorgu(self):
        query = """
        SELECT m.MalzemeAdi, m.StokAdet, t.FirmaAdi, p.AdSoyad as TeslimAlan, tk.TedarikTarihi
        FROM dbo.Malzemeler m
        LEFT JOIN dbo.TedarikKayitlari tk ON m.MalzemeID = tk.MalzemeID
        LEFT JOIN dbo.Tedarikciler t ON tk.TedarikciID = t.TedarikciID
        LEFT JOIN dbo.Personeller p ON tk.PersonelID = p.PersonelID
        """
        self.show_veri_tablosu("Detaylı Depo Sorgu Ekranı", query)

    # --- LOJİSTİK BÖLÜMÜ  ---
    def setup_lojistik(self):
        frame = tk.Frame(self.tab_lojistik)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="LOJİSTİK YÖNETİM PANELİ", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(frame, text="Lojistik Yetkili Girişi", width=25, height=2, bg="#d35400", fg="white", font='bold',
                  command=lambda: self.login_window("mehmettunc", "mehmet07032", self.show_lojistik_paneli)).pack()

    def show_lojistik_paneli(self):
        query = "SELECT FirmaAdi, YetkiliKisi, Telefon, Adres FROM dbo.Tedarikciler"
        self.show_veri_tablosu("Tedarikçi Listesi", query)

    # ---  SATIN ALMA BÖLÜMÜ ---
    def setup_satin_alma(self):
        frame = tk.Frame(self.tab_satin_alma)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Button(frame, text="Sisteme Giriş", width=20, bg="#8e44ad", fg="white", command=lambda: self.login_window("serifeadatunc", "serife07032", self.satin_alma_yonetim)).pack(pady=10)
        tk.Button(frame, text="Hızlı Satış (Göz At)", width=20, command=self.satin_alma_satis).pack(pady=10)
        tk.Button(frame, text="İletişim Bilgileri", width=20, command=self.satin_alma_iletisim).pack(pady=10)

    def satin_alma_yonetim(self):
        top = tk.Toplevel(self.root)
        top.title("Satın Alma Paneli")
        top.geometry("700x550")
        
        sn = ttk.Notebook(top)
        sn.pack(expand=True, fill='both')
        
        f_alim = ttk.Frame(sn); f_satim = ttk.Frame(sn); f_mesaj = ttk.Frame(sn)
        sn.add(f_alim, text="Alım İşlemleri"); sn.add(f_satim, text="Satış Takip"); sn.add(f_mesaj, text="Mesajlar")

        tk.Label(f_alim, text="KRİTİK STOK UYARISI (3'ten Az)", fg="red", font=("Arial", 10, "bold")).pack(pady=5)
        self.create_treeview(f_alim, "SELECT MalzemeAdi, StokAdet FROM dbo.Malzemeler WHERE StokAdet < 3")
        
        tk.Label(f_alim, text="\nTEDARİKÇİ İLETİŞİM LİSTESİ", font=("Arial", 10, "bold")).pack(pady=5)
        self.create_treeview(f_alim, "SELECT FirmaAdi, YetkiliKisi, Telefon FROM dbo.Tedarikciler")

        # Mesaj Bölümü
        tk.Label(f_mesaj, text="Fikirleriniz bizim için önemli (Maks. 10.000 Karakter)").pack(pady=10)
        txt = scrolledtext.ScrolledText(f_mesaj, width=60, height=12)
        txt.pack(padx=10)
        tk.Button(f_mesaj, text="Mesajı Gönder", bg="#2980b9", fg="white", command=lambda: messagebox.showinfo("DEPOM", "Mesajınız alınmıştır.")).pack(pady=10)

    def satin_alma_satis(self):
        top = tk.Toplevel(self.root)
        top.title("Satış & Sepet")
        top.geometry("500x650")
        
        tk.Label(top, text=f"Sipariş Kodu: {self.siparis_kodu}", font=("Courier", 12, "bold"), fg="red").pack(pady=10)
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MalzemeAdi, StokAdet FROM dbo.Malzemeler")
            for row in cursor.fetchall():
                f = tk.Frame(top, relief="groove", borderwidth=1, pady=5)
                f.pack(fill="x", padx=20, pady=3)
                tk.Label(f, text=f"{row[0]} | Fiyat: 10€", font="Arial 9").pack(side="left", padx=5)
                tk.Button(f, text="Sepete Ekle", bg="#f1c40f", command=lambda r=row: self.sepete_ekle(r[0], r[1])).pack(side="right", padx=5)
            conn.close()
        else:
            tk.Label(top, text="Veritabanı bağlantısı yok!", fg="red").pack()

        tk.Button(top, text="ÖDEME EKRANINA GİT", bg="#27ae60", fg="white", font="bold", height=2, command=self.odeme_ekrani).pack(pady=20)

    def odeme_ekrani(self):
        top = tk.Toplevel(self.root)
        top.title("Ödeme Onay")
        top.geometry("450x500")

        tutar = len(self.sepet) * 10
        tk.Label(top, text=f"Sepet Toplamı: {tutar}€", font=("Arial", 18, "bold"), fg="#2c3e50").pack(pady=20)

        # Adres Girişi ve Placeholder
        addr_frame = tk.Frame(top)
        addr_frame.pack(pady=10)
        
        addr = tk.Entry(addr_frame, fg="grey", width=45, font="Arial 10 italic")
        addr.insert(0, "lütfen adresi giriniz")
        
        def handle_focus_in(e):
            if addr.get() == "lütfen adresi giriniz":
                addr.delete(0, tk.END)
                addr.config(fg="black", font="Arial 10")

        addr.bind("<FocusIn>", handle_focus_in)
        addr.pack(ipady=5)

        def final_onay():
            if addr.get() == "" or addr.get() == "lütfen adresi giriniz":
                messagebox.showwarning("Uyarı", "Lütfen adres giriniz!")
                return
            
            iban = "TR" + "".join([str(random.randint(0,9)) for _ in range(24)])
            tel = "05" + "".join([str(random.randint(0,9)) for _ in range(9)])
            bilgi = f"IBAN: {iban}\nTelefon: {tel}\n\nSipariş kodunuz ({self.siparis_kodu}) ile dekont gönderdiğinizde sipariş onaylanacaktır. Bizimle iletişime geçebilirsiniz."
            messagebox.showinfo("Sipariş Alındı", bilgi)
            top.destroy()

        tk.Button(top, text="SİPARİŞİ ONAYLA", bg="#2ecc71", fg="white", font="bold", command=final_onay, width=20, height=2).pack(pady=30)

    # ---  PERSONELLER BÖLÜMÜ ---
    def setup_personel(self):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT AdSoyad, Gorev, Telefon FROM dbo.Personeller")
            rows = cursor.fetchall()
            for r in rows:
                p_frame = tk.Frame(self.tab_personeller, pady=10, relief="flat")
                p_frame.pack(fill="x", padx=50)
                tk.Label(p_frame, text=r[1], font=("Arial", 10, "bold"), fg="#e74c3c").pack(anchor="w")
                tk.Label(p_frame, text=f"{r[0]}  ---  İletişim: {r[2]}", font=("Arial", 11)).pack(anchor="w")
            conn.close()

    def satin_alma_iletisim(self):
        mail = f"depom_iletisim_{random.randint(100,999)}@gmail.com"
        tel = f"0212 {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}"
        messagebox.showinfo("İletişim", f"Müşteri Hizmetleri: {tel}\nE-Posta: {mail}")

    # --- YARDIMCI ---
    def login_window(self, u_name, u_pwd, success_func):
        win = tk.Toplevel(self.root)
        win.title("Güvenli Giriş")
        win.geometry("350x300")
        win.grab_set() 
        
        tk.Label(win, text="\nSİSTEM GİRİŞİ", font="Arial 12 bold").pack()
        tk.Label(win, text="Kullanıcı Adı:").pack(pady=(20,0))
        entry_u = tk.Entry(win, width=25)
        entry_u.pack()
        
        tk.Label(win, text="Şifre:").pack(pady=(10,0))
        entry_p = tk.Entry(win, show="*", width=25)
        entry_p.pack()
        
        def attempt():
            if entry_u.get() == u_name and entry_p.get() == u_pwd:
                win.destroy()
                success_func()
            else:
                messagebox.showerror("Hata", "Giriş başarısız! Bilgilerinizi kontrol edin.")
        
        tk.Button(win, text="Giriş Yap", bg="#34495e", fg="white", width=15, command=attempt).pack(pady=25)

    def sepete_ekle(self, urun, stok):
        count = self.sepet.count(urun)
        if count >= stok:
            messagebox.showwarning("Stok Sınırı", f"Üzgünüz, {urun} ürününden depoda başka kalmadı! Son ürün sepetinizde.")
        else:
            self.sepet.append(urun)
            messagebox.showinfo("Sepet", f"{urun} başarıyla eklendi.")

    def show_veri_tablosu(self, baslik, sql_sorgu):
        win = tk.Toplevel(self.root)
        win.title(baslik)
        win.geometry("800x450")
        self.create_treeview(win, sql_sorgu)

    def create_treeview(self, parent, sql_sorgu):
        conn = get_db_connection()
        if not conn:
            tk.Label(parent, text="Veritabanı Hatası! Lütfen Bağlantıyı Kontrol Edin.", fg="red").pack()
            return
            
        cursor = conn.cursor()
        cursor.execute(sql_sorgu)
        
        basliklar = [desc[0] for desc in cursor.description]
        tree = ttk.Treeview(parent, columns=basliklar, show='headings')
        
        for b in basliklar:
            tree.heading(b, text=b)
            tree.column(b, width=150, anchor="center")
            
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=list(row))
            
        tree.pack(expand=True, fill='both', padx=15, pady=15)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DepomApp(root)
    root.mainloop()
