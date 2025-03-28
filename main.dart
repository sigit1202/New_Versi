import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = "Tekan tombol dan mulai berbicara";
  String apiUrl = "https://your-render-api-url.com/search"; // Ganti dengan URL dari Render.com

  List<dynamic> resultsSheet1 = [];
  List<dynamic> resultsSheet2 = [];

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
  }

Future<void> searchData(String query1, String query2) async {
  final response = await http.get(Uri.parse("$apiUrl?query1=$query1&query2=$query2"));

  if (response.statusCode == 200) {
    var data = json.decode(response.body);
    setState(() {
      resultsSheet1 = data["sheet1_results"] ?? [];
      resultsSheet2 = data["sheet2_results"] ?? [];
    });
  } else {
    throw Exception("Gagal mengambil data");
  }
}


  void _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize(
        onStatus: (val) => print("Status: $val"),
        onError: (val) => print("Error: $val"),
      );

      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (val) => setState(() {
            _text = val.recognizedWords;
          }),
          localeId: "id_ID",
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
      if (_text.isNotEmpty) {
        searchData(_text);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("Pencarian Data")),
        floatingActionButton: FloatingActionButton(
          onPressed: _listen,
          child: Icon(_isListening ? Icons.mic : Icons.mic_none),
        ),
        body: Column(
          children: [
            Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                _text,
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
            ),
            Expanded(
              child: ListView(
                children: [
                  Text("📌 Hasil dari Sheet 1", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  ...resultsSheet1.map((item) => ListTile(
                        title: Text(
                          "📅 ${item['Tanggal Bulan dan Tahun']}\n📍 ${item['Kota Asal']} ➝ ${item['Kota Tujuan']}\n📦 STT: ${item['Jumlah STT']} | Berat: ${item['Jumlah Berat']} | Revenue: ${item['Jumlah Revenue']}",
                          style: TextStyle(fontSize: 14),
                        ),
                      )),
                  SizedBox(height: 20),
                  Text("📌 Hasil dari Sheet 2", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  ...resultsSheet2.map((item) => ListTile(
                        title: Text(
                          "🌍 Negara: ${item['Negara']} (${item['3 Letter Code']})\n👤 PIC: ${item['Nama PIC']} | Owner: ${item['Nama Owner']} (${item['Profesi Owner']})\n📞 ${item['Nomor Owner']} | 🏠 ${item['Alamat Owner']}",
                          style: TextStyle(fontSize: 14),
                        ),
                      )),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
