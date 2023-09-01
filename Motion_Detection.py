import cv2
from datetime import datetime

# Motion_Detection / Hareket algılama

def farkImaj(t0, t1, t2):
    # İki ardışık karenin farkını alır
    fark1 = cv2.absdiff(t2, t1)
    fark2 = cv2.absdiff(t1, t0)
    # İki farklı fark görüntüsünün bitwise and işlemi yapılır
    return cv2.bitwise_and(fark1, fark2)

# Hareket algılama eşiği - bu eşiği değiştirerek algılama hassasiyetini ayarlayabilirsiniz
esik_deger = 140000

# Kamera yakalanır
kamera = cv2.VideoCapture(0)

# Pencere ismi oluşturulur
pencereIsmi = "Motion_Detection"
cv2.namedWindow(pencereIsmi)

# Üç ardışık çerçeve için başlangıç çerçeveleri yakalanır
t_eksi = cv2.cvtColor(kamera.read()[1], cv2.COLOR_BGR2GRAY)
t = cv2.cvtColor(kamera.read()[1], cv2.COLOR_BGR2GRAY)
t_arti = cv2.cvtColor(kamera.read()[1], cv2.COLOR_BGR2GRAY)

# Zaman kontrolü için başlangıç zamanı alınır
zamanKontrol = datetime.now().strftime('%Ss')

while True:
    # Kameradan bir kare alınır ve pencerede gösterilir
    cv2.imshow(pencereIsmi, kamera.read()[1])
    
    # İki ardışık kare arasındaki fark hesaplanır ve eşik değeri ile karşılaştırılır
    if cv2.countNonZero(farkImaj(t_eksi, t, t_arti)) > esik_deger and zamanKontrol != datetime.now().strftime('%Ss'):
        # Eşik değeri aşılırsa, farklı bir kare yakalanır ve kaydedilir
        fark_resim = kamera.read()[1]
        cv2.imwrite(datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg', fark_resim)
        
    # Zaman kontrolü güncellenir
    zamanKontrol = datetime.now().strftime('%Ss')
    
    # Ardışık kareler güncellenir
    t_eksi = t
    t = t_arti
    t_arti = cv2.cvtColor(kamera.read()[1], cv2.COLOR_BGR2GRAY)
    
    # 'Esc' tuşuna basıldığında döngüyü sonlandırır ve pencereyi kapatır
    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyWindow(pencereIsmi)
        break
