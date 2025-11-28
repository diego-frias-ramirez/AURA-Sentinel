// location_service.dart
import 'package:geolocator/geolocator.dart';

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  Position? _currentPosition;
  Stream<Position>? _positionStream;

  // Solicitar permisos de ubicación
  Future<bool> requestPermission() async {
    try {
      LocationPermission permission = await Geolocator.checkPermission();

      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }

      if (permission == LocationPermission.deniedForever) {
        return false;
      }

      return permission == LocationPermission.whileInUse ||
          permission == LocationPermission.always;
    } catch (e) {
      print('❌ Error solicitando permisos de ubicación: $e');
      return false;
    }
  }

  // Obtener ubicación actual
  Future<Position?> getCurrentLocation() async {
    try {
      bool hasPermission = await requestPermission();
      if (!hasPermission) return null;

      _currentPosition = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      return _currentPosition;
    } catch (e) {
      print('❌ Error obteniendo ubicación: $e');
      return null;
    }
  }

  // Iniciar seguimiento en tiempo real
  Stream<Position>? getLocationStream() {
    try {
      _positionStream = Geolocator.getPositionStream(
        locationSettings: const LocationSettings(
          accuracy: LocationAccuracy.high,
          distanceFilter: 10, // metros
        ),
      );
      return _positionStream;
    } catch (e) {
      print('❌ Error iniciando stream de ubicación: $e');
      return null;
    }
  }

  // Detener seguimiento
  void stopLocationTracking() {
    _positionStream = null;
  }

  // Calcular distancia entre dos puntos
  double calculateDistance(
    double startLat,
    double startLng,
    double endLat,
    double endLng,
  ) {
    return Geolocator.distanceBetween(startLat, startLng, endLat, endLng);
  }

  // Obtener dirección a partir de coordenadas
  Future<String> getAddressFromCoordinates(double lat, double lng) async {
    try {
      // TODO: Implementar usando geocoding
      // List<Placemark> placemarks = await placemarkFromCoordinates(lat, lng);
      // if (placemarks.isNotEmpty) {
      //   Placemark place = placemarks.first;
      //   return '${place.street}, ${place.locality}, ${place.country}';
      // }

      // Simulación
      await Future.delayed(const Duration(milliseconds: 200));
      return 'Calle Principal 123, Ciudad';
    } catch (e) {
      print('❌ Error obteniendo dirección: $e');
      return 'Ubicación no disponible';
    }
  }

  Position? get currentPosition => _currentPosition;
}
