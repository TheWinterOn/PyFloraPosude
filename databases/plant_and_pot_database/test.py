from PIL import Image

biljka = ["Hoya", "databases/plant_database/plant_photos/hoya.jpg"]
image = Image.open(biljka[1])

image.show()
