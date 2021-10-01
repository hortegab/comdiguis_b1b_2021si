#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SER Simulation
# Author: Homero Ortega Boada
# Description: Dale un valor a Es/No, corre el flujograma y obten la SER. Puedes sacar tantos valores como para construir una curva de SER
# GNU Radio version: 3.9.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from b_demod_constelacion_cb import b_demod_constelacion_cb  # grc-generated hier_block
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import epy_block_0
import epy_block_1
import math
import numpy as np



from gnuradio import qtgui

class ser_simulation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SER Simulation", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SER Simulation")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ser_simulation")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.const0 = const0 = digital.constellation_qpsk().points()
        self.samp_rate = samp_rate = 100e3
        self.Sps = Sps = 1
        self.M0 = M0 = len(const0)
        self.run_stop = run_stop = True
        self.mapa = mapa = np.arange(M0)
        self.Rs = Rs = samp_rate/Sps
        self.N_snr = N_snr = 32
        self.MaxErrors = MaxErrors = 1000
        self.MaxCount = MaxCount = int(1e7)
        self.EsN0min = EsN0min = -5
        self.EsN0max = EsN0max = 25

        ##################################################
        # Blocks
        ##################################################
        _run_stop_check_box = Qt.QCheckBox('Inicial/Parar')
        self._run_stop_choices = {True: True, False: False}
        self._run_stop_choices_inv = dict((v,k) for k,v in self._run_stop_choices.items())
        self._run_stop_callback = lambda i: Qt.QMetaObject.invokeMethod(_run_stop_check_box, "setChecked", Qt.Q_ARG("bool", self._run_stop_choices_inv[i]))
        self._run_stop_callback(self.run_stop)
        _run_stop_check_box.stateChanged.connect(lambda i: self.set_run_stop(self._run_stop_choices[bool(i)]))
        self.top_grid_layout.addWidget(_run_stop_check_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            N_snr,
            EsN0min,
            (EsN0max-EsN0min)/float(N_snr),
            "Es/N0 [dB]",
            "logPe",
            "Curva de sER",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-8, 0)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("dB")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ["qPSK", "QPSK", '8PSK', "16QAM", '',
            '', '', '', '', '']
        widths = [4, 4, 4, 4, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_1 = epy_block_1.blk(N=32)
        self.epy_block_0 = epy_block_0.blk(N=N_snr, EsN0min=EsN0min, EsN0max=EsN0max, Sps=Sps, Rs=Rs)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc(const0, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, N_snr)
        self.blocks_stream_to_vector_0_1_0 = blocks.stream_to_vector(gr.sizeof_char*1, N_snr)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_char*1, N_snr)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N_snr)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, N_snr, 0)
        self.b_demod_constelacion_cb_0 = b_demod_constelacion_cb(
            Constelacion=const0,
        )
        self.analog_random_source_x_1 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, M0, 10000000))), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_1, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.analog_random_source_x_1, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.b_demod_constelacion_cb_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.b_demod_constelacion_cb_0, 0), (self.blocks_stream_to_vector_0_1_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_stream_to_vector_0_1_0, 0), (self.epy_block_1, 1))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.b_demod_constelacion_cb_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_nlog10_ff_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ser_simulation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_const0(self):
        return self.const0

    def set_const0(self, const0):
        self.const0 = const0
        self.set_M0(len(self.const0))
        self.b_demod_constelacion_cb_0.set_Constelacion(self.const0)
        self.digital_chunks_to_symbols_xx_1.set_symbol_table(self.const0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_Rs(self.samp_rate/self.Sps)

    def get_Sps(self):
        return self.Sps

    def set_Sps(self, Sps):
        self.Sps = Sps
        self.set_Rs(self.samp_rate/self.Sps)

    def get_M0(self):
        return self.M0

    def set_M0(self, M0):
        self.M0 = M0
        self.set_mapa(np.arange(self.M0))

    def get_run_stop(self):
        return self.run_stop

    def set_run_stop(self, run_stop):
        self.run_stop = run_stop
        if self.run_stop: self.start()
        else: self.stop(); self.wait()
        self._run_stop_callback(self.run_stop)

    def get_mapa(self):
        return self.mapa

    def set_mapa(self, mapa):
        self.mapa = mapa

    def get_Rs(self):
        return self.Rs

    def set_Rs(self, Rs):
        self.Rs = Rs

    def get_N_snr(self):
        return self.N_snr

    def set_N_snr(self, N_snr):
        self.N_snr = N_snr
        self.qtgui_vector_sink_f_0.set_x_axis(self.EsN0min, (self.EsN0max-self.EsN0min)/float(self.N_snr))

    def get_MaxErrors(self):
        return self.MaxErrors

    def set_MaxErrors(self, MaxErrors):
        self.MaxErrors = MaxErrors

    def get_MaxCount(self):
        return self.MaxCount

    def set_MaxCount(self, MaxCount):
        self.MaxCount = MaxCount

    def get_EsN0min(self):
        return self.EsN0min

    def set_EsN0min(self, EsN0min):
        self.EsN0min = EsN0min
        self.qtgui_vector_sink_f_0.set_x_axis(self.EsN0min, (self.EsN0max-self.EsN0min)/float(self.N_snr))

    def get_EsN0max(self):
        return self.EsN0max

    def set_EsN0max(self, EsN0max):
        self.EsN0max = EsN0max
        self.qtgui_vector_sink_f_0.set_x_axis(self.EsN0min, (self.EsN0max-self.EsN0min)/float(self.N_snr))




def main(top_block_cls=ser_simulation, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
