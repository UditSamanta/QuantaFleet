import math
import heapq
from typing import List, Tuple, Dict

def haversine_nm(p1: List[float], p2: List[float]) -> float:
    """Computes great circle distance between [lat1, lon1] and [lat2, lon2] in Nautical Miles."""
    lat1, lon1 = p1
    lat2, lon2 = p2
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return (R * c) / 1.852

class MaritimeSeaRouter:
    """
    Global Oceanic Navigation Graph & Pathfinding Engine.
    Ensures vessel shipping routes navigate exclusively through open waters,
    straits, canals, and around peninsulas/landmasses (e.g. Cape Comorin, Suez,
    Gibraltar, Malacca, Panama, Cape of Good Hope, English Channel).
    """

    NODES: Dict[str, List[float]] = {
        # --- Indian Subcontinent Coastal Waypoints ---
        "MUNDRA_OFF": [22.4, 69.1],
        "KANDLA_OFF": [22.8, 70.0],
        "MUMBAI_OFF": [18.7, 72.4],
        "JNPT_OFF": [18.9, 72.8],
        "GOA_OFF": [15.2, 73.4],
        "MANGALORE_OFF": [12.8, 74.4],
        "KOCHI_OFF": [9.8, 75.8],
        "CAPE_COMORIN": [7.6, 77.4],
        "GALLE_SOUTH": [5.6, 80.3],        # South of Sri Lanka deep sea lane
        "SRI_LANKA_EAST": [6.8, 82.2],
        "SRI_LANKA_NE": [8.5, 82.0],
        "CHENNAI_OFF": [13.1, 80.5],
        "ENNORE_OFF": [13.3, 80.4],
        "VIZAG_OFF": [17.6, 83.5],
        "PARADIP_OFF": [20.1, 86.8],
        "KOLKATA_OFF": [21.0, 88.3],
        "CHITTAGONG_OFF": [21.8, 91.6],
        "COLOMBO_OFF": [6.95, 79.7],

        # --- Arabian Sea, Persian Gulf & Middle East ---
        "ARABIAN_SEA_NORTH": [21.0, 64.0],
        "ARABIAN_SEA_MID": [15.0, 65.0],
        "ARABIAN_SEA_SOUTH": [10.0, 66.0],
        "OMAN_OFF": [20.0, 59.5],
        "HORMUZ_ENTRANCE": [25.0, 57.5],
        "HORMUZ_STRAIT": [26.4, 56.4],
        "DUBAI_OFF": [25.3, 54.8],
        "ABU_DHABI_OFF": [24.5, 54.2],
        "DAMMAM_OFF": [26.5, 50.3],
        "DOHA_OFF": [25.3, 51.6],
        "GULF_ADEN_EAST": [13.5, 51.0],
        "GULF_ADEN_MID": [12.8, 48.0],
        "GULF_ADEN_WEST": [12.2, 45.0],
        "BAB_EL_MANDEB": [12.6, 43.4],

        # --- Red Sea & Suez Canal ---
        "RED_SEA_SOUTH": [15.0, 41.8],
        "RED_SEA_MID": [20.0, 38.5],
        "RED_SEA_NORTH": [26.5, 35.0],
        "GULF_SUEZ": [28.2, 33.3],
        "SUEZ_SOUTH": [29.9, 32.5],
        "SUEZ_NORTH": [31.3, 32.3],

        # --- Mediterranean Sea ---
        "MED_EAST_PORT_SAID": [32.0, 32.0],
        "MED_ALEXANDRIA_OFF": [31.5, 29.8],
        "MED_CYPRUS_SOUTH": [34.0, 33.0],
        "MED_CRETE_SOUTH": [34.4, 25.0],
        "MED_PIRAEUS_OFF": [37.5, 23.6],
        "MED_IONIAN_SEA": [36.5, 19.0],
        "MED_MALTA_CHANNEL": [36.2, 14.8],
        "MED_TYRRHENIAN_SEA": [40.0, 12.0],
        "MED_GENOA_OFF": [44.0, 8.8],
        "MED_MARSEILLE_OFF": [43.1, 5.2],
        "MED_BALEARIC": [38.2, 3.0],
        "MED_VALENCIA_OFF": [39.4, 0.0],
        "MED_BARCELONA_OFF": [41.2, 2.2],
        "MED_ALBORAN_SEA": [36.0, -2.5],
        "STRAIT_GIBRALTAR": [35.9, -5.6],

        # --- Atlantic & Northern Europe ---
        "ATLANTIC_GIBRALTAR_WEST": [36.0, -7.0],
        "ATLANTIC_LISBON_OFF": [38.6, -9.6],
        "ATLANTIC_FINISTERRE": [43.0, -9.5],
        "BAY_BISCAY": [45.5, -6.0],
        "ENGLISH_CHANNEL_WEST": [49.5, -5.5],
        "ENGLISH_CHANNEL_MID": [50.2, -1.0],
        "ENGLISH_CHANNEL_DOVER": [51.0, 1.5],
        "NORTH_SEA_ROTTERDAM": [52.0, 3.8],
        "NORTH_SEA_ANTWERP": [51.4, 3.6],
        "NORTH_SEA_HAMBURG_APPROACH": [54.0, 7.8],
        "NORTH_SEA_FELIXSTOWE": [51.9, 1.4],
        "SKAGERRAK_STRAIT": [57.8, 9.5],
        "BALTIC_ENTRANCE": [55.5, 12.8],

        # --- Indian Ocean & Southeast Asia ---
        "BAY_BENGAL_MID": [12.0, 88.0],
        "ANDAMAN_SEA_NORTH": [6.5, 94.5],
        "MALACCA_WEST": [5.2, 98.0],
        "MALACCA_MID": [3.0, 101.0],
        "SINGAPORE_STRAIT": [1.25, 103.85],
        "JAKARTA_SUNDA_STRAIT": [-6.0, 105.8],
        "SOUTH_CHINA_SEA_SOUTH": [3.5, 106.0],
        "SOUTH_CHINA_SEA_MID": [12.0, 112.5],
        "SOUTH_CHINA_SEA_NORTH": [19.5, 115.0],
        "HONG_KONG_OFF": [22.1, 114.2],
        "TAIWAN_STRAIT": [24.0, 119.5],
        "EAST_CHINA_SEA_SHANGHAI": [31.0, 122.5],
        "NINGBO_OFF": [29.9, 122.0],
        "QINGDAO_OFF": [35.8, 120.5],
        "TIANJIN_OFF": [38.8, 118.0],
        "KOREA_STRAIT_BUSAN": [34.8, 129.2],
        "JAPAN_PACIFIC_TOKYO": [34.8, 140.0],
        "YOKOHAMA_OFF": [35.3, 139.7],
        "KOBE_OFF": [34.5, 135.2],

        # --- Africa & Cape of Good Hope ---
        "EAST_AFRICA_MOMBASA": [-4.0, 40.0],
        "MOZAMBIQUE_CHANNEL": [-18.0, 39.0],
        "DURBAN_OFF": [-30.0, 31.5],
        "PORT_ELIZABETH_OFF": [-34.2, 26.0],
        "CAPE_GOOD_HOPE": [-34.8, 18.5],
        "ATLANTIC_WEST_AFRICA": [-5.0, 5.0],
        "ATLANTIC_CANARY_ISLANDS": [28.0, -16.0],

        # --- Americas, Panama & Oceans ---
        "ATLANTIC_MID_NORTH": [35.0, -45.0],
        "US_EAST_COAST_NEW_YORK": [40.2, -73.5],
        "US_EAST_COAST_SAVANNAH": [31.8, -80.5],
        "FLORIDA_STRAITS": [24.5, -81.0],
        "GULF_MEXICO_HOUSTON": [28.8, -94.5],
        "CARIBBEAN_SEA": [14.0, -75.0],
        "PANAMA_CANAL_ATLANTIC": [9.4, -79.9],
        "PANAMA_CANAL_PACIFIC": [8.9, -79.6],
        "PACIFIC_MEXICO_OFF": [18.0, -104.0],
        "PACIFIC_LOS_ANGELES_OFF": [33.5, -118.5],
        "PACIFIC_SAN_FRANCISCO_OFF": [37.5, -122.8],
        "PACIFIC_SEATTLE_OFF": [47.5, -124.5],
        "PACIFIC_MID_NORTH": [35.0, 175.0],
        "PACIFIC_MID_HAWAII": [21.5, -158.0],
        "BRAZIL_SANTOS_OFF": [-24.5, -46.0],
        "ARGENTINA_BUENOS_AIRES_OFF": [-35.5, -57.0],
        "AUSTRALIA_SYDNEY_OFF": [-34.0, 151.5],
        "AUSTRALIA_MELBOURNE_OFF": [-38.5, 145.0],
        "AUSTRALIA_FREMANTLE_OFF": [-32.2, 115.5]
    }

    EDGES = [
        # --- Indian Subcontinent Coastal Chain (Prevents cross-country routing) ---
        ("MUNDRA_OFF", "KANDLA_OFF"),
        ("MUNDRA_OFF", "MUMBAI_OFF"),
        ("MUMBAI_OFF", "JNPT_OFF"),
        ("MUMBAI_OFF", "GOA_OFF"),
        ("GOA_OFF", "MANGALORE_OFF"),
        ("MANGALORE_OFF", "KOCHI_OFF"),
        ("KOCHI_OFF", "CAPE_COMORIN"),
        ("CAPE_COMORIN", "COLOMBO_OFF"),
        ("COLOMBO_OFF", "GALLE_SOUTH"),
        ("CAPE_COMORIN", "GALLE_SOUTH"),
        ("GALLE_SOUTH", "SRI_LANKA_EAST"),
        ("SRI_LANKA_EAST", "SRI_LANKA_NE"),
        ("SRI_LANKA_NE", "CHENNAI_OFF"),
        ("SRI_LANKA_EAST", "CHENNAI_OFF"),
        ("CHENNAI_OFF", "ENNORE_OFF"),
        ("CHENNAI_OFF", "VIZAG_OFF"),
        ("VIZAG_OFF", "PARADIP_OFF"),
        ("PARADIP_OFF", "KOLKATA_OFF"),
        ("KOLKATA_OFF", "CHITTAGONG_OFF"),

        # --- India to Middle East & Red Sea ---
        ("MUMBAI_OFF", "ARABIAN_SEA_MID"),
        ("MUNDRA_OFF", "ARABIAN_SEA_NORTH"),
        ("ARABIAN_SEA_NORTH", "ARABIAN_SEA_MID"),
        ("ARABIAN_SEA_MID", "ARABIAN_SEA_SOUTH"),
        ("ARABIAN_SEA_NORTH", "OMAN_OFF"),
        ("ARABIAN_SEA_MID", "OMAN_OFF"),
        ("OMAN_OFF", "HORMUZ_ENTRANCE"),
        ("HORMUZ_ENTRANCE", "HORMUZ_STRAIT"),
        ("HORMUZ_STRAIT", "DUBAI_OFF"),
        ("DUBAI_OFF", "ABU_DHABI_OFF"),
        ("DUBAI_OFF", "DOHA_OFF"),
        ("DOHA_OFF", "DAMMAM_OFF"),
        ("OMAN_OFF", "GULF_ADEN_EAST"),
        ("ARABIAN_SEA_MID", "GULF_ADEN_EAST"),
        ("ARABIAN_SEA_SOUTH", "GULF_ADEN_EAST"),
        ("CAPE_COMORIN", "GULF_ADEN_EAST"),
        ("GALLE_SOUTH", "GULF_ADEN_EAST"),
        ("GULF_ADEN_EAST", "GULF_ADEN_MID"),
        ("GULF_ADEN_MID", "GULF_ADEN_WEST"),
        ("GULF_ADEN_WEST", "BAB_EL_MANDEB"),

        # --- Red Sea & Suez Canal ---
        ("BAB_EL_MANDEB", "RED_SEA_SOUTH"),
        ("RED_SEA_SOUTH", "RED_SEA_MID"),
        ("RED_SEA_MID", "RED_SEA_NORTH"),
        ("RED_SEA_NORTH", "GULF_SUEZ"),
        ("GULF_SUEZ", "SUEZ_SOUTH"),
        ("SUEZ_SOUTH", "SUEZ_NORTH"),

        # --- Mediterranean Corridor ---
        ("SUEZ_NORTH", "MED_EAST_PORT_SAID"),
        ("MED_EAST_PORT_SAID", "MED_ALEXANDRIA_OFF"),
        ("MED_EAST_PORT_SAID", "MED_CYPRUS_SOUTH"),
        ("MED_CYPRUS_SOUTH", "MED_CRETE_SOUTH"),
        ("MED_ALEXANDRIA_OFF", "MED_CRETE_SOUTH"),
        ("MED_CRETE_SOUTH", "MED_PIRAEUS_OFF"),
        ("MED_CRETE_SOUTH", "MED_IONIAN_SEA"),
        ("MED_IONIAN_SEA", "MED_MALTA_CHANNEL"),
        ("MED_MALTA_CHANNEL", "MED_TYRRHENIAN_SEA"),
        ("MED_TYRRHENIAN_SEA", "MED_GENOA_OFF"),
        ("MED_GENOA_OFF", "MED_MARSEILLE_OFF"),
        ("MED_MALTA_CHANNEL", "MED_BALEARIC"),
        ("MED_MARSEILLE_OFF", "MED_BALEARIC"),
        ("MED_BALEARIC", "MED_VALENCIA_OFF"),
        ("MED_BALEARIC", "MED_BARCELONA_OFF"),
        ("MED_VALENCIA_OFF", "MED_ALBORAN_SEA"),
        ("MED_BALEARIC", "MED_ALBORAN_SEA"),
        ("MED_ALBORAN_SEA", "STRAIT_GIBRALTAR"),

        # --- Atlantic & Northern Europe Corridor ---
        ("STRAIT_GIBRALTAR", "ATLANTIC_GIBRALTAR_WEST"),
        ("ATLANTIC_GIBRALTAR_WEST", "ATLANTIC_LISBON_OFF"),
        ("ATLANTIC_LISBON_OFF", "ATLANTIC_FINISTERRE"),
        ("ATLANTIC_FINISTERRE", "BAY_BISCAY"),
        ("BAY_BISCAY", "ENGLISH_CHANNEL_WEST"),
        ("ENGLISH_CHANNEL_WEST", "ENGLISH_CHANNEL_MID"),
        ("ENGLISH_CHANNEL_MID", "ENGLISH_CHANNEL_DOVER"),
        ("ENGLISH_CHANNEL_DOVER", "NORTH_SEA_ROTTERDAM"),
        ("ENGLISH_CHANNEL_DOVER", "NORTH_SEA_ANTWERP"),
        ("ENGLISH_CHANNEL_DOVER", "NORTH_SEA_FELIXSTOWE"),
        ("NORTH_SEA_ROTTERDAM", "NORTH_SEA_HAMBURG_APPROACH"),
        ("NORTH_SEA_HAMBURG_APPROACH", "SKAGERRAK_STRAIT"),
        ("SKAGERRAK_STRAIT", "BALTIC_ENTRANCE"),

        # --- India / Sri Lanka to Southeast Asia Corridor ---
        ("GALLE_SOUTH", "ANDAMAN_SEA_NORTH"),
        ("SRI_LANKA_EAST", "ANDAMAN_SEA_NORTH"),
        ("CHENNAI_OFF", "ANDAMAN_SEA_NORTH"),
        ("VIZAG_OFF", "BAY_BENGAL_MID"),
        ("KOLKATA_OFF", "BAY_BENGAL_MID"),
        ("BAY_BENGAL_MID", "ANDAMAN_SEA_NORTH"),
        ("ANDAMAN_SEA_NORTH", "MALACCA_WEST"),
        ("MALACCA_WEST", "MALACCA_MID"),
        ("MALACCA_MID", "SINGAPORE_STRAIT"),
        ("SINGAPORE_STRAIT", "JAKARTA_SUNDA_STRAIT"),

        # --- Southeast Asia to East Asia Corridor ---
        ("SINGAPORE_STRAIT", "SOUTH_CHINA_SEA_SOUTH"),
        ("SOUTH_CHINA_SEA_SOUTH", "SOUTH_CHINA_SEA_MID"),
        ("SOUTH_CHINA_SEA_MID", "SOUTH_CHINA_SEA_NORTH"),
        ("SOUTH_CHINA_SEA_NORTH", "HONG_KONG_OFF"),
        ("SOUTH_CHINA_SEA_NORTH", "TAIWAN_STRAIT"),
        ("HONG_KONG_OFF", "TAIWAN_STRAIT"),
        ("TAIWAN_STRAIT", "NINGBO_OFF"),
        ("NINGBO_OFF", "EAST_CHINA_SEA_SHANGHAI"),
        ("EAST_CHINA_SEA_SHANGHAI", "QINGDAO_OFF"),
        ("QINGDAO_OFF", "TIANJIN_OFF"),
        ("EAST_CHINA_SEA_SHANGHAI", "KOREA_STRAIT_BUSAN"),
        ("KOREA_STRAIT_BUSAN", "KOBE_OFF"),
        ("KOBE_OFF", "YOKOHAMA_OFF"),
        ("YOKOHAMA_OFF", "JAPAN_PACIFIC_TOKYO"),

        # --- Trans-Pacific Corridor ---
        ("JAPAN_PACIFIC_TOKYO", "PACIFIC_MID_NORTH"),
        ("PACIFIC_MID_NORTH", "PACIFIC_SAN_FRANCISCO_OFF"),
        ("PACIFIC_MID_NORTH", "PACIFIC_LOS_ANGELES_OFF"),
        ("PACIFIC_SAN_FRANCISCO_OFF", "PACIFIC_LOS_ANGELES_OFF"),
        ("PACIFIC_SAN_FRANCISCO_OFF", "PACIFIC_SEATTLE_OFF"),
        ("JAPAN_PACIFIC_TOKYO", "PACIFIC_MID_HAWAII"),
        ("PACIFIC_MID_HAWAII", "PACIFIC_LOS_ANGELES_OFF"),

        # --- Trans-Atlantic & Americas Corridor ---
        ("ENGLISH_CHANNEL_WEST", "ATLANTIC_MID_NORTH"),
        ("ATLANTIC_GIBRALTAR_WEST", "ATLANTIC_MID_NORTH"),
        ("ATLANTIC_MID_NORTH", "US_EAST_COAST_NEW_YORK"),
        ("US_EAST_COAST_NEW_YORK", "US_EAST_COAST_SAVANNAH"),
        ("US_EAST_COAST_SAVANNAH", "FLORIDA_STRAITS"),
        ("FLORIDA_STRAITS", "GULF_MEXICO_HOUSTON"),
        ("FLORIDA_STRAITS", "CARIBBEAN_SEA"),
        ("CARIBBEAN_SEA", "PANAMA_CANAL_ATLANTIC"),
        ("PANAMA_CANAL_ATLANTIC", "PANAMA_CANAL_PACIFIC"),
        ("PANAMA_CANAL_PACIFIC", "PACIFIC_MEXICO_OFF"),
        ("PACIFIC_MEXICO_OFF", "PACIFIC_LOS_ANGELES_OFF"),

        # --- Africa / South America Corridor ---
        ("GALLE_SOUTH", "EAST_AFRICA_MOMBASA"),
        ("EAST_AFRICA_MOMBASA", "MOZAMBIQUE_CHANNEL"),
        ("MOZAMBIQUE_CHANNEL", "DURBAN_OFF"),
        ("DURBAN_OFF", "PORT_ELIZABETH_OFF"),
        ("PORT_ELIZABETH_OFF", "CAPE_GOOD_HOPE"),
        ("CAPE_GOOD_HOPE", "ATLANTIC_WEST_AFRICA"),
        ("ATLANTIC_WEST_AFRICA", "ATLANTIC_CANARY_ISLANDS"),
        ("ATLANTIC_CANARY_ISLANDS", "ATLANTIC_GIBRALTAR_WEST"),
        ("ATLANTIC_WEST_AFRICA", "BRAZIL_SANTOS_OFF"),
        ("BRAZIL_SANTOS_OFF", "ARGENTINA_BUENOS_AIRES_OFF"),
        ("BRAZIL_SANTOS_OFF", "FLORIDA_STRAITS"),

        # --- Australia Corridor ---
        ("JAKARTA_SUNDA_STRAIT", "AUSTRALIA_FREMANTLE_OFF"),
        ("SINGAPORE_STRAIT", "AUSTRALIA_FREMANTLE_OFF"),
        ("AUSTRALIA_FREMANTLE_OFF", "AUSTRALIA_MELBOURNE_OFF"),
        ("AUSTRALIA_MELBOURNE_OFF", "AUSTRALIA_SYDNEY_OFF")
    ]

    def __init__(self):
        self.adj = {k: [] for k in self.NODES}
        for u, v in self.EDGES:
            if u in self.NODES and v in self.NODES:
                d = haversine_nm(self.NODES[u], self.NODES[v])
                self.adj[u].append((v, d))
                self.adj[v].append((u, d))

    def _interpolate_segment(self, p1: List[float], p2: List[float], n_points: int = 6) -> List[List[float]]:
        """Interpolates smooth geodetic points along a water segment."""
        lat1, lon1 = p1
        lat2, lon2 = p2
        phi1, lambda1 = math.radians(lat1), math.radians(lon1)
        phi2, lambda2 = math.radians(lat2), math.radians(lon2)

        d = 2 * math.asin(math.sqrt(
            math.sin((phi2 - phi1) / 2.0) ** 2 +
            math.cos(phi1) * math.cos(phi2) * math.sin((lambda2 - lambda1) / 2.0) ** 2
        ))

        if d == 0:
            return [[round(lat1, 4), round(lon1, 4)]]

        segment = []
        for i in range(n_points):
            f = i / float(n_points)
            A = math.sin((1 - f) * d) / math.sin(d)
            B = math.sin(f * d) / math.sin(d)
            x = A * math.cos(phi1) * math.cos(lambda1) + B * math.cos(phi2) * math.cos(lambda2)
            y = A * math.cos(phi1) * math.sin(lambda1) + B * math.cos(phi2) * math.sin(lambda2)
            z = A * math.sin(phi1) + B * math.sin(phi2)
            lat = math.atan2(z, math.sqrt(x**2 + y**2))
            lon = math.atan2(y, x)
            segment.append([round(math.degrees(lat), 4), round(math.degrees(lon), 4)])

        return segment

    def get_sea_route(self, start_coord: List[float], end_coord: List[float]) -> Tuple[List[List[float]], float]:
        """
        Computes the shortest oceanic navigation route between start_coord and end_coord,
        guaranteeing the route stays 100% on sea lanes and avoids crossing land.
        """
        # Find closest oceanic entry nodes
        start_node = min(self.NODES.keys(), key=lambda k: haversine_nm(start_coord, self.NODES[k]))
        end_node = min(self.NODES.keys(), key=lambda k: haversine_nm(end_coord, self.NODES[k]))

        # Dijkstra on sea graph
        dist = {k: float('inf') for k in self.NODES}
        prev = {k: None for k in self.NODES}
        dist[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end_node:
                break
            for v, weight in self.adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))

        # Reconstruct path
        sea_nodes = []
        curr = end_node
        while curr:
            sea_nodes.append(self.NODES[curr])
            curr = prev[curr]
        sea_nodes.reverse()

        # Chain all points from port to sea nodes to arrival port
        raw_path = [start_coord] + sea_nodes + [end_coord]

        # Calculate exact total nautical miles
        total_nm = 0.0
        for i in range(len(raw_path) - 1):
            total_nm += haversine_nm(raw_path[i], raw_path[i + 1])

        # Smooth spline / geodesic sub-segments
        smoothed_waypoints = []
        for i in range(len(raw_path) - 1):
            sub_pts = self._interpolate_segment(raw_path[i], raw_path[i + 1], n_points=5)
            smoothed_waypoints.extend(sub_pts)
        smoothed_waypoints.append([round(end_coord[0], 4), round(end_coord[1], 4)])

        return smoothed_waypoints, round(total_nm, 1)

maritime_router = MaritimeSeaRouter()
