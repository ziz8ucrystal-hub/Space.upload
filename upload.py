import os
import yt_dlp
import asyncio
from telegram import Bot

BOT_TOKEN = "8763050525:AAGjCizH6kCuWJc4e8tt6TKaSMRDYgA1hxQ"
CHANNEL_ID = "@JF_Ziz8u"

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

async def main():
    print(f"🚀 بدء رفع {len(VIDEOS)} فيديو كملفات...")
    bot = Bot(token=BOT_TOKEN)
    
    for i, video in enumerate(VIDEOS, 1):
        try:
            print(f"\n[{i}/{len(VIDEOS)}] 📥 {video['title']}")
            filename = f"{video['title']}.mp4"
            
            # تحميل الفيديو
            ydl_opts = {
                'format': 'best[height<=720]',  # يمكنك تغيير الجودة
                'outtmpl': filename,
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video['url']])
            
            # رفع كملف (Document)
            if os.path.exists(filename):
                size = os.path.getsize(filename) / (1024 * 1024)
                print(f"✅ تم التحميل ({size:.1f} MB)")
                print("📤 جاري الرفع كملف...")
                
                with open(filename, 'rb') as f:
                    await bot.send_document(
                        chat_id=CHANNEL_ID,
                        document=f,
                        caption=f"📹 {video['title']}\n📁 الحجم: {size:.1f} MB\n✅ تم الرفع كملف"
                    )
                
                print(f"✅ تم رفع {video['title']}")
                
                # مسح الملف
                os.remove(filename)
                print(f"🗑️ تم مسح الملف المؤقت")
            else:
                print("❌ فشل التحميل")
            
            # انتظار قليل
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ خطأ في {video['title']}: {e}")
    
    print("\n" + "="*50)
    print("✨ تم الانتهاء من رفع جميع الفيديوهات!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())