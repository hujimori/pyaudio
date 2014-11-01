#coding: utf-8
import wave
import pyaudio
import struct
import numpy as np
from pylab import*

class Pywave:

	
	def printWaveInfo(self):
		# waveファイルの情報の取得
		print "チャンネル数:", self.wf.getnchannels()
		print "サンプル幅:", self.wf.getsampwidth()
		print "サンプリング周波数:", self.wf.getframerate()
		print "フレーム数:", self.wf.getnframes()
		print "パラメータ:", self.wf.getparams()
		print "長さ(秒):", float(self.wf.getnframes()) / self.wf.getframerate()

	def openStream(self):
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(self.wf.getsampwidth()), 
		                channels = self.wf.getnchannels(), rate = self.wf.getframerate(), output = True)
		chunk = 1024
		data = self.wf.readframes(chunk)
		while data != '':
			stream.write(data)
			data = self.wf.readframes(chunk)
		stream.close()
		p.terminate()

	def createSineWave(self, A, f0, fs, length):
		data = []
		for n in arange(length * fs):
			s = A * np.sin(2 * np.pi * f0 * n / fs)
			if s > 1.0: s = 1.0
			if s < -1.0: s = -1.0
			data.append(s)
		data = [int(x * 32767.0) for x in data]
		data = struct.pack("h" * len(data), *data)
		return data

	def createCombineWave(self, A, freqList, fs, length):
		data = []
		amp = float(A) / len(freqList)
		for n in arange(length * fs):
			s = 0.0
			for f in freqList:
				s += amp * np.sin(2 * np.pi * f * n / fs)
			if s > 1.0: s = 1.0
			if s < -1.0: s = -1.0
			data.append(s)
		data = [int(x * 32767.0) for x in data]
		data = struct.pack("h" * len (data), *data)
		return data

	def createTriangleWave(self, A, f0, fs, length):
		data = []
		for n in arange(length * fs):
			s = 0.0
			for k in range(0, 10):
				s += (-1)**k * (A / (2*k+1)**2) * np.sin((2*k+1) * 2 * np.pi * f0 * n / fs)
			if s > 1.0: s = 1.0
			if s < -1.0: s = -1.0
			data.append(s)
		data = [int(x * 32767.0) for x in data]
		data = struct.pack("h" * len(data), *data)
		return data

	def createSquareWave(self, A, f0, fs, length):
		data = []
		for n in arange(length * fs):
			s = 0.0
			for k in range(1, 10):
				s += (A / (2 * k - 1)) * np.sin((2 * k - 1) * 2 * np.pi * f0 * n / fs)
			if s > 1.0: s = 1.0
			if s < -1.0: s = -1.0
			data.append(s)
		data = [int(x * 32767.0) for x in data]
		data = struct.pack("h" * len(data), *data)
		return data

	def createSawtoothWave(self, A, f0, fs, length):
		data = []
		for n in arange(length * fs):
			s = 0.0
			for k in range(1, 10):
				s += (A / K) * np.sin(2 * np.pi * k * f0 * n / fs)
			if s > 1.0: s = 1.0
			if s < -1.0: s = -1.0
			data.append(s)
		data = [int(x * 32767.0) for x in data]
		plot(data[0:100])
		show()

		data = struct.pack("h" * len(data), *data)
		return data

	def play(self, data, fs, bit):
		p = pyaudio.PyAudio()
		stream = p.open(format = pyaudio.paInt16, channels = 1, rate = int(fs), output = True)
		chunk = 1024
		sp = 0
		buffer = data[sp:sp+chunk]
		while buffer != '':
			stream.write(buffer)
			sp = sp + chunk
			buffer = data[sp:sp+chunk]
		stream.close()
		p.terminate()


	def save(self, data, fs, bit, filename):
		# 波形データをWAVEファイルｈ出力
		wf = wave.open(filename, "w")
		wf.setnchannels(1)
		wf.setsampwidth(bit / 8)
		wf.setframerate(fs)
		wf.writeframes(data)
		wf.close()

	def createDft(self, start, x, N):
		# xのstartサンプル目からのNサンプルを周期波形とみなしたDFTを返す
		X = [0.0] * N
		for k in range(N):
			for n in range(N):
				real = np.cos(2 * np.pi * k *n / N)
				imag = -np.sin(2 * np.pi * k * n / N)
				X[k] += x[start + n] * complex(real, imag)
		return X

	def plot(self):
		buffer = self.wf.readframes(self.wf.getnframes())
		print len(buffer) # バイト数 = 1フレーム × フレーム数

		# bufferはバイナリなので2バイトずつ整数にまとめる
		data = frombuffer(buffer, dtype = "int16")

		#プロット
		plot(data[0:200])
		show()
