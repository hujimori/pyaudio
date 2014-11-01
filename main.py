#coding: utf-8
import wave
import pyaudio
import pywave
import numpy as np
from pylab import*


if __name__ == '__main__':
	chordList = [(262, 330, 392),  # C（ドミソ）
				(294, 370, 440),  # D（レファ#ラ）
				(330, 415, 494),  # E（ミソ#シ）
				(349, 440, 523),  # F（ファラド）
				(392, 494, 587),  # G（ソシレ）
				(440, 554, 659),  # A（ラド#ミ）
				(494, 622, 740)]  # B（シレ#ファ#）

	#freqList = [262, 294, 330, 349, 392, 440, 494, 523] # ドレミファソラシド
	
	allData = ""

	wf = wave.open("./sine.wav", "r");
	pw = pywave.Pywave()
	fs = wf.getframerate() # サンプリング周波数
	x = wf.readframes(wf.getnframes())
	x = frombuffer(x, dtype = "int16") / 32768.0 # -1 - +1に正規化した波形
	print len(x)
	wf.close()

	start = 0 # サンプリングする開始位置
	N = 256   # サンプル数
	X = pw.createDft(start, x, N) # 離散フーリエ変換
	freqList = [k * fs / N for k in range(N)] # 周波数のリスト
	amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X] # 振幅スペクトル np.abs()
	phaseSpectrum = [np.arctan2(int(c.imag), int(c.real)) for c in X] 	# 位相スペクトル np.angle()
	
	# 波形サンプルを描画
	subplot(311) # 3行一列のグラフの1番目の位置にプロット
	plot(range(start, start + N), x[start:start+N])
	axis([start, start + N, -1.0, 1.0])
	xlabel("time [sample]")
	ylabel("amplitude")

	# 振幅スペクトルを描画
	subplot(312)
	plot(freqList, amplitudeSpectrum, marker = 'o', linestyle = '-')
	axis([0, fs / 2 , 0, 15])
	xlabel("frequency  [Hz]")
	ylabel("amplitude spectrum")

	# 位相スペクトルを描画
	subplot(313)
	plot(freqList, amplitudeSpectrum, marker = 'o', linestyle = '-')
	axis([0, fs / 2, -np.pi, np.pi])
	xlabel("frequency [Hz]")
	ylabel("amplitude spectrum")

	show()
	for f in chordList:
		data = createSineWave(1.0, f, 8000.0, 1.0)
		pw.play(data, 8000, 16)
#	for f in freqList:
#		data = pw.createSineWave(1.0, f, 8000.0, 1.0)
		#data = pw.createTriangleWave(0.5, f, 8000.0, 1.0)
		#data = pw.createCombineWave(1.0, f, 8000.0, 1.0)
		#data = pw.createSquareWave(0.5, f, 8000.0, 1.0)
		#data = createSawtoothWave(0.5, f, 8000.0, 1.0)
#		pw.play(data, 8000, 16)
#		allData += data
#	pw.save(allData, 8000, 16, "sine.wav")