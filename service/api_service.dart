import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String apiUrl = "https://new-versi.onrender.com/search";

  static Future<List<dynamic>> searchData(String query) async {
    try {
      final response = await http.get(Uri.parse('$apiUrl?query=$query'));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception("Gagal mengambil data: ${response.statusCode}");
      }
    } catch (e) {
      throw Exception("Terjadi kesalahan: $e");
    }
  }
}
