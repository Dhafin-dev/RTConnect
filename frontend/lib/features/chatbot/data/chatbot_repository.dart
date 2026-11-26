import '../../../core/network/api_client.dart';
import '../../../core/network/api_endpoints.dart';

class ChatbotRepository {
  final ApiClient _apiClient;

  ChatbotRepository({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  Future<Map<String, dynamic>> sendQuery({
    required String query,
    int? sessionId,
  }) async {
    final response = await _apiClient.dio.post<Map<String, dynamic>>(
      ApiEndpoints.chatbotQuery,
      data: {
        'query': query,
        if (sessionId != null) 'session_id': sessionId,
      },
    );
    return Map<String, dynamic>.from(response.data!['data'] as Map);
  }

  Future<List<Map<String, dynamic>>> getSessions() async {
    final response = await _apiClient.dio.get<Map<String, dynamic>>('/chatbot/sessions');
    final data = response.data!['data'] as List;
    return data.map((e) => Map<String, dynamic>.from(e as Map)).toList();
  }

  Future<List<Map<String, dynamic>>> getSessionMessages(int sessionId) async {
    final response = await _apiClient.dio.get<Map<String, dynamic>>('/chatbot/sessions/$sessionId/messages');
    final data = response.data!['data'] as List;
    return data.map((e) => Map<String, dynamic>.from(e as Map)).toList();
  }

  Future<List<Map<String, dynamic>>> getKnowledgeDocuments() async {
    final response = await _apiClient.dio.get<Map<String, dynamic>>('/chatbot/knowledge');
    final data = response.data!['data'] as List;
    return data.map((e) => Map<String, dynamic>.from(e as Map)).toList();
  }

  Future<Map<String, dynamic>> createKnowledgeDocument({
    required String judul,
    required String kategori,
    required String isiDokumen,
    String sumber = 'SOP Resmi RT',
  }) async {
    final response = await _apiClient.dio.post<Map<String, dynamic>>(
      '/chatbot/knowledge',
      data: {
        'judul': judul,
        'kategori': kategori,
        'isi_dokumen': isiDokumen,
        'sumber': sumber,
      },
    );
    return Map<String, dynamic>.from(response.data!['data'] as Map);
  }

  Future<Map<String, dynamic>> updateKnowledgeDocument({
    required int knowledgeId,
    required String judul,
    required String kategori,
    required String isiDokumen,
    String sumber = 'SOP Resmi RT',
  }) async {
    final response = await _apiClient.dio.put<Map<String, dynamic>>(
      '/chatbot/knowledge/$knowledgeId',
      data: {
        'judul': judul,
        'kategori': kategori,
        'isi_dokumen': isiDokumen,
        'sumber': sumber,
      },
    );
    return Map<String, dynamic>.from(response.data!['data'] as Map);
  }

  Future<void> deleteKnowledgeDocument(int knowledgeId) async {
    await _apiClient.dio.delete<Map<String, dynamic>>('/chatbot/knowledge/$knowledgeId');
  }
}
