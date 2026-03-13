import os
import yt_dlp
import requests
import json
from datetime import datetime

# ========== توكن بوت تليجرام ==========
BOT_TOKEN = "8763050525:AAGjCizH6kCuWJc4e8tt6TKaSMRDYgA1hxQ"
CHANNEL_ID = "7283912673"  # حسابك الشخصي - البوت يرسل لك هنا

# ========== قائمة الفيديوهات ==========
VIDEOS = [
    {"url": "https://player.vimeo.com/video/1043974638", "title": "01_Trading_View"},
    {"url": "https://player.vimeo.com/video/1064144416", "title": "02_Risk_Management_P1"},
    {"url": "https://player.vimeo.com/video/1043876016", "title": "03_The_Basics_Part_4"},
    {"url": "https://player.vimeo.com/video/1044120961", "title": "04_The_Basics_Part_3"},
    {"url": "https://player.vimeo.com/video/1043976446", "title": "05_Time_Frame"},
    {"url": "https://player.vimeo.com/video/1044120914", "title": "06_The_Basics_Part_2"},
    {"url": "https://player.vimeo.com/video/1044120852", "title": "07_The_Basics_Part_1"},
    {"url": "https://player.vimeo.com/video/1045168170", "title": "08_Volume_Profile"},
    {"url": "https://player.vimeo.com/video/1045167024", "title": "09_Order_Block_1"},
    {"url": "https://player.vimeo.com/video/1043974824", "title": "10_Price_Action"},
    {"url": "https://player.vimeo.com/video/1043983996", "title": "11_Market_Structure"},
    {"url": "https://player.vimeo.com/video/1043971382", "title": "12_Consolidation"},
    {"url": "https://player.vimeo.com/video/1043976568", "title": "13_Fair_Value_Gap"},
    {"url": "https://player.vimeo.com/video/1043974689", "title": "14_OB"},
    {"url": "https://player.vimeo.com/video/1043971955", "title": "15_Stop_Loss"},
    {"url": "https://player.vimeo.com/video/1043974778", "title": "16_Psychology"},
    {"url": "https://player.vimeo.com/video/1043973455", "title": "17_Welcome"},
    {"url": "https://player.vimeo.com/video/1043976498", "title": "18_What_is_Risk_Management"},
    {"url": "https://player.vimeo.com/video/1043974742", "title": "19_Stop_Hunt"},
    {"url": "https://vimeo.com/1086214885?share=copy", "title": "20_P1_Psychology1"},
    {"url": "https://vimeo.com/1086211587?share=copy", "title": "21_P2_Price_Action"},
    {"url": "https://vimeo.com/1086214933?share=copy", "title": "22_P2_Psychology2"},
    {"url": "https://vimeo.com/1086215569?share=copy", "title": "23_P1_Stop_Hunt_01"},
    {"url": "https://vimeo.com/1086215684?share=copy", "title": "24_P2_Stop_Hunt_02"},
    {"url": "https://vimeo.com/1086215458?share=copy", "title": "25_P1_Tp"},
    {"url": "https://vimeo.com/1086215516?share=copy", "title": "26_P2_Tpsl02"},
    {"url": "https://vimeo.com/1086209786?share=copy", "title": "27_P1_Volume_P_01"},
    {"url": "https://vimeo.com/1086210242/7b545c33d4", "title": "28_P2_Volume_P_02"},
    {"url": "https://vimeo.com/1086207541?share=copy", "title": "29_P1_Order_Block_01"},
    {"url": "https://vimeo.com/1086207587?share=copy", "title": "30_P2_Order_Block_02"},
    {"url": "https://vimeo.com/1086211265?share=copy", "title": "31_P1_Price_Action_01"},
]

# ========== دالة رفع إلى GoFile.io ==========
def upload_to_gofile(filepath):
    """رفع الملف إلى GoFile.io"""
    try:
        # الحصول على أفضل سيرفر
        print("🔍 البحث عن أفضل سيرفر...")
        server_response = requests.get('https://api.gofile.io/servers', timeout=10)
        
        if server_response.status_code == 200:
            server_data = server_response.json()
            if server_data['status'] == 'ok' and server_data.get('data', {}).get('servers'):
                server = server_data['data']['servers'][0]['name']
                print(f"✅ تم اختيار السيرفر: {server}")
            else:
                server = 'store1'
                print("⚠️ استخدام السيرفر الافتراضي: store1")
        else:
            server = 'store1'
            print("⚠️ استخدام السيرفر الافتراضي: store1")
        
        # رفع الملف
        print(f"📤 رفع الملف إلى {server}.gofile.io...")
        
        with open(filepath, 'rb') as f:
            response = requests.post(
                f'https://{server}.gofile.io/uploadFile',
                files={'file': f},
                timeout=300
            )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok' and 'data' in data:
                if 'downloadPage' in data['data']:
                    return data['data']['downloadPage']
                elif 'fileId' in data['data']:
                    return f"https://gofile.io/d/{data['data']['fileId']}"
        return None
    except Exception as e:
        print(f"❌ خطأ في الرفع: {e}")
        return None

# ========== دالة إرسال رسالة تليجرام ==========
def send_telegram(message):
    """إرسال رسالة إلى حسابك الشخصي"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print("✅ تم إرسال الرسالة إلى حسابك")
            return True
        else:
            print(f"❌ خطأ في الإرسال: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

# ========== الدالة الرئيسية ==========
def main():
    print("="*50)
    print(f"🚀 بدء رفع {len(VIDEOS)} فيديو إلى GoFile.io")
    print("="*50)
    
    send_telegram(f"🚀 بدء رفع {len(VIDEOS)} فيديو إلى GoFile.io")
    
    successful = 0
    failed = 0
    
    for i, video in enumerate(VIDEOS, 1):
        print(f"\n[{i}/{len(VIDEOS)}] 📥 {video['title']}")
        
        filename = f"video_{i}.mp4"
        
        try:
            # تحميل الفيديو من Vimeo
            print("📥 جاري التحميل من Vimeo...")
            ydl_opts = {
                'format': 'best[height<=480]',
                'outtmpl': filename,
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video['url']])
            
            # التحقق من التحميل
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                size_mb = os.path.getsize(filename) / (1024 * 1024)
                print(f"✅ تم التحميل ({size_mb:.1f} MB)")
                
                # رفع إلى GoFile.io
                link = upload_to_gofile(filename)
                
                if link:
                    # إرسال الرابط إلى حسابك
                    message = (
                        f"🎬 <b>{video['title']}</b>\n"
                        f"📁 الحجم: {size_mb:.1f} MB\n"
                        f"✅ تم الرفع إلى GoFile.io\n"
                        f"🔗 <a href='{link}'>رابط التحميل</a>"
                    )
                    if send_telegram(message):
                        print(f"✅ تم رفع {video['title']}")
                        successful += 1
                    else:
                        failed += 1
                else:
                    print(f"❌ فشل الرفع إلى GoFile.io")
                    failed += 1
                
                # حذف الملف المؤقت
                try:
                    os.remove(filename)
                    print(f"🗑️ تم حذف الملف المؤقت")
                except:
                    pass
            else:
                print(f"❌ فشل التحميل من Vimeo")
                failed += 1
                
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
            failed += 1
    
    # التقرير النهائي
    summary = (
        f"✨ <b>تم الانتهاء من الرفع</b>\n"
        f"✅ نجح: {successful}\n"
        f"❌ فشل: {failed}"
    )
    send_telegram(summary)
    
    print("\n" + "="*50)
    print(f"✅ تم بنجاح: {successful}")
    print(f"❌ فشل: {failed}")
    print("="*50)

if __name__ == "__main__":
    main()