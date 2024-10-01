import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:influencer_map/models/content.dart';
import 'package:influencer_map/models/place.dart';
import 'package:influencer_map/res/strings.dart';
import 'package:influencer_map/res/text_styles.dart';
import 'package:influencer_map/routes/home.dart';
import 'package:lottie/lottie.dart';
import '../models/influencer.dart';
import '../src/constants.dart' as constants;
import 'package:http/http.dart' as http;

class DataLoading extends StatefulWidget {
  const DataLoading({super.key});

  @override
  State<DataLoading> createState() => _DataLoadingState();
}

class _DataLoadingState extends State<DataLoading> {
  final List<Influencer> influencers = [];
  final List<Place> places = [];
  final List<Content> contents = [];

  @override
  void initState() {
    loadContentsMarkers();
    super.initState();
  }

  Future<void> loadContentsMarkers() async {
    await fetchInfluencers().then((data) {
      influencers.addAll(data);
    });

    await fetchPlaces().then((data) {
      places.addAll(data);
    });

    await fetchContents().then((data) {
      contents.addAll(data);
    });

    print("## places length: ${places.length}");
    print("## contents length: ${contents.length}");

    await Future.delayed(const Duration(seconds: 1));

    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => Home(
            influencers: influencers,
            places: places,
            contents: contents,
          ),
        ),
      );
    }
  }

  Future<List<Influencer>> fetchInfluencers() async {
    final response = await http.get(constants.fetchInfluencersUri);

    if (response.statusCode == constants.httpStatusOk) {
      return parseInfluencers(utf8.decode(response.bodyBytes));
      // return compute(parsePlaces, response.body);
    } else {
      throw Exception('Failed to load influencers');
    }
  }

  Future<List<Place>> fetchPlaces() async {
    final response = await http.get(constants.fetchPlacesUri);

    if (response.statusCode == constants.httpStatusOk) {
      return parsePlaces(utf8.decode(response.bodyBytes));
    } else {
      throw Exception('Failed to load places');
    }
  }

  Future<List<Content>> fetchContents() async {
    final response = await http.get(constants.fetchContentsUri);

    if (response.statusCode == constants.httpStatusOk) {
      return parseContents(utf8.decode(response.bodyBytes));
    } else {
      throw Exception('Failed to load places');
    }
  }

  List<Influencer> parseInfluencers(String responseBody) {
    final parsed = jsonDecode(responseBody).cast<Map<String, dynamic>>();
    return parsed.map<Influencer>((json) => Influencer.fromJson(json)).toList();
  }

  List<Place> parsePlaces(String responseBody) {
    final parsed = jsonDecode(responseBody).cast<Map<String, dynamic>>();
    return parsed.map<Place>((json) => Place.fromJson(json)).toList();
  }

  List<Content> parseContents(String responseBody) {
    final parsed = jsonDecode(responseBody).cast<Map<String, dynamic>>();
    return parsed.map<Content>((json) => Content.fromJson(json)).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Wrap(
          spacing: 40,
          direction: Axis.vertical,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            SizedBox(
                width: 100,
                height: 100,
                child: Lottie.asset('assets/lottie/food-carousel.json')),
            const Text(
              MyStrings.loadData,
              style: MyTextStyles.medium,
            ),
          ],
        ),
      ),
    );
  }
}
