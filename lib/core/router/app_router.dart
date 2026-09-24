import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'route_names.dart';

// Screens Import
import '../../features/auth/presentation/landing_screen.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/auth/presentation/register_screen.dart';
import '../../features/home/presentation/warga_home_screen.dart';
import '../../features/home/presentation/rt_home_screen.dart';
import '../../features/letters/presentation/letter_application_screen.dart';
import '../../features/letters/presentation/letter_history_screen.dart';
import '../../features/letters/presentation/letter_detail_screen.dart';
import '../../features/letters/presentation/rt_review_screen.dart';
import '../../features/letters/presentation/pdf_viewer_screen.dart';
import '../../features/chatbot/presentation/chatbot_screen.dart';
import '../../features/notifications/presentation/notification_feed_screen.dart';

final GlobalKey<NavigatorState> rootNavigatorKey = GlobalKey<NavigatorState>();

final GoRouter appRouter = GoRouter(
  navigatorKey: rootNavigatorKey,
  initialLocation: RouteNames.landing,
  routes: [
    // Landing & Auth
    GoRoute(
      path: RouteNames.landing,
      builder: (context, state) => const LandingScreen(),
    ),
    GoRoute(
      path: RouteNames.login,
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: RouteNames.register,
      builder: (context, state) => const RegisterScreen(),
    ),

    // Warga Routes
    GoRoute(
      path: RouteNames.wargaHome,
      builder: (context, state) => const WargaHomeScreen(),
    ),
    GoRoute(
      path: RouteNames.wargaPengajuan,
      builder: (context, state) => const LetterHistoryScreen(),
    ),
    GoRoute(
      path: RouteNames.wargaPengajuanBaru,
      builder: (context, state) => const LetterApplicationScreen(),
    ),
    GoRoute(
      path: '/letters/:id',
      builder: (context, state) {
        final id = int.tryParse(state.pathParameters['id'] ?? '0') ?? 0;
        return LetterDetailScreen(applicationId: id);
      },
    ),

    // RT Routes
    GoRoute(
      path: RouteNames.rtHome,
      builder: (context, state) => const RTHomeScreen(),
    ),
    GoRoute(
      path: RouteNames.rtQueue,
      builder: (context, state) => const RTReviewScreen(),
    ),

    // PDF Preview
    GoRoute(
      path: '/surat/preview/:id',
      builder: (context, state) {
        final id = int.tryParse(state.pathParameters['id'] ?? '0') ?? 0;
        return PdfViewerScreen(applicationId: id);
      },
    ),

    // Chatbot & Notifications
    GoRoute(
      path: RouteNames.chatbot,
      builder: (context, state) => const ChatbotScreen(),
    ),
    GoRoute(
      path: RouteNames.notifications,
      builder: (context, state) => const NotificationFeedScreen(),
    ),
  ],
);
