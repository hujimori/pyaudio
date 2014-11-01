import pywave

pw = pywave.Pywave()
data = pw.createSineWave(0.25, 250, 8000.0, 1.0)
pw.save(data, 8000, 16, "sine.wav")