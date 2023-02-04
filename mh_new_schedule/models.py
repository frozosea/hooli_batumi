from typing import List, Any, Optional, Dict, TypeVar, Callable, Type, cast
from enum import Enum
from datetime import datetime
import dateutil.parser

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


class IDs:
    cities: int
    districts: List[int]
    streets: List[Any]
    regions: List[Any]

    def __init__(self, cities: int, districts: List[int], streets: List[Any], regions: List[Any]) -> None:
        self.cities = cities
        self.districts = districts
        self.streets = streets
        self.regions = regions

    @staticmethod
    def from_dict(obj: Any) -> 'IDs':
        assert isinstance(obj, dict)
        cities = int(from_str(obj.get("Cities")))
        districts = from_list(lambda x: int(from_str(x)), obj.get("Districts"))
        streets = from_list(lambda x: x, obj.get("Streets"))
        regions = from_list(lambda x: x, obj.get("Regions"))
        return IDs(cities, districts, streets, regions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Cities"] = from_str(str(self.cities))
        result["Districts"] = from_list(lambda x: from_str((lambda x: str(x))(x)), self.districts)
        result["Streets"] = from_list(lambda x: x, self.streets)
        result["Regions"] = from_list(lambda x: x, self.regions)
        return result


class Name:
    ru: str
    name_def: Optional[str]
    ka: str
    en: str

    def __init__(self, ru: str, name_def: Optional[str], ka: str, en: str) -> None:
        self.ru = ru
        self.name_def = name_def
        self.ka = ka
        self.en = en

    @staticmethod
    def from_dict(obj: Any) -> 'Name':
        assert isinstance(obj, dict)
        ru = from_str(obj.get("ru"))
        name_def = from_union([from_str, from_none], obj.get("def"))
        ka = from_str(obj.get("ka"))
        en = from_str(obj.get("en"))
        return Name(ru, name_def, ka, en)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ru"] = from_str(self.ru)
        result["def"] = from_union([from_str, from_none], self.name_def)
        result["ka"] = from_str(self.ka)
        result["en"] = from_str(self.en)
        return result


class LOC:
    name: Name
    children: None

    def __init__(self, name: Name, children: None) -> None:
        self.name = name
        self.children = children

    @staticmethod
    def from_dict(obj: Any) -> 'LOC':
        assert isinstance(obj, dict)
        name = Name.from_dict(obj.get("name"))
        children = from_none(obj.get("children"))
        return LOC(name, children)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_class(Name, self.name)
        result["children"] = from_none(self.children)
        return result


class Districts:
    i_ds: IDs
    locs: Dict[str, LOC]

    def __init__(self, i_ds: IDs, locs: Dict[str, LOC]) -> None:
        self.i_ds = i_ds
        self.locs = locs

    @staticmethod
    def from_dict(obj: Any) -> 'Districts':
        assert isinstance(obj, dict)
        i_ds = IDs.from_dict(obj.get("IDs"))
        locs = from_dict(LOC.from_dict, obj.get("Locs"))
        return Districts(i_ds, locs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["IDs"] = to_class(IDs, self.i_ds)
        result["Locs"] = from_dict(lambda x: to_class(LOC, x), self.locs)
        return result


class Floor:
    developer_flat_id: int
    product_id: int
    floor: int
    price: str
    price_value: str
    currency_id: int

    def __init__(self, developer_flat_id: int, product_id: int, floor: int, price: str, price_value: str,
                 currency_id: int) -> None:
        self.developer_flat_id = developer_flat_id
        self.product_id = product_id
        self.floor = floor
        self.price = price
        self.price_value = price_value
        self.currency_id = currency_id

    @staticmethod
    def from_dict(obj: Any) -> 'Floor':
        assert isinstance(obj, dict)
        developer_flat_id = int(from_str(obj.get("developer_flat_id")))
        product_id = int(from_str(obj.get("product_id")))
        floor = int(from_str(obj.get("floor")))
        price = from_str(obj.get("price"))
        price_value = from_str(obj.get("price_value"))
        currency_id = int(from_str(obj.get("currency_id")))
        return Floor(developer_flat_id, product_id, floor, price, price_value, currency_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["developer_flat_id"] = from_str(str(self.developer_flat_id))
        result["product_id"] = from_str(str(self.product_id))
        result["floor"] = from_str(str(self.floor))
        result["price"] = from_str(self.price)
        result["price_value"] = from_str(self.price_value)
        result["currency_id"] = from_str(str(self.currency_id))
        return result


class ParentLOCCenter:
    lon: str
    lat: str

    def __init__(self, lon: str, lat: str) -> None:
        self.lon = lon
        self.lat = lat

    @staticmethod
    def from_dict(obj: Any) -> 'ParentLOCCenter':
        assert isinstance(obj, dict)
        lon = from_str(obj.get("lon"))
        lat = from_str(obj.get("lat"))
        return ParentLOCCenter(lon, lat)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lon"] = from_str(self.lon)
        result["lat"] = from_str(self.lat)
        return result


class Geometry:
    coordinates: List[List[List[float]]]
    type: str

    def __init__(self, coordinates: List[List[List[float]]], type: str) -> None:
        self.coordinates = coordinates
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Geometry':
        assert isinstance(obj, dict)
        coordinates = from_list(lambda x: from_list(lambda x: from_list(from_float, x), x), obj.get("coordinates"))
        type = from_str(obj.get("type"))
        return Geometry(coordinates, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coordinates"] = from_list(lambda x: from_list(lambda x: from_list(to_float, x), x), self.coordinates)
        result["type"] = from_str(self.type)
        return result


class ParentLOC:
    osm_id: int
    parent_osm_id: int
    level: int
    subs: int
    center: ParentLOCCenter
    right: int
    type: str
    seo_title: Name
    depth: int
    left: int
    admin_level: int
    name: Name
    pathway: Name
    rank: int
    geometry: Geometry
    parent_loc_class: str
    sort: None
    score: int

    def __init__(self, osm_id: int, parent_osm_id: int, level: int, subs: int, center: ParentLOCCenter, right: int,
                 type: str, seo_title: Name, depth: int, left: int, admin_level: int, name: Name, pathway: Name,
                 rank: int, geometry: Geometry, parent_loc_class: str, sort: None, score: int) -> None:
        self.osm_id = osm_id
        self.parent_osm_id = parent_osm_id
        self.level = level
        self.subs = subs
        self.center = center
        self.right = right
        self.type = type
        self.seo_title = seo_title
        self.depth = depth
        self.left = left
        self.admin_level = admin_level
        self.name = name
        self.pathway = pathway
        self.rank = rank
        self.geometry = geometry
        self.parent_loc_class = parent_loc_class
        self.sort = sort
        self.score = score

    @staticmethod
    def from_dict(obj: Any) -> 'ParentLOC':
        assert isinstance(obj, dict)
        osm_id = from_int(obj.get("osm_id"))
        parent_osm_id = from_int(obj.get("parent_osm_id"))
        level = from_int(obj.get("level"))
        subs = from_int(obj.get("subs"))
        center = ParentLOCCenter.from_dict(obj.get("center"))
        right = from_int(obj.get("right"))
        type = from_str(obj.get("type"))
        seo_title = Name.from_dict(obj.get("seo_title"))
        depth = from_int(obj.get("depth"))
        left = from_int(obj.get("left"))
        admin_level = int(from_str(obj.get("admin_level")))
        name = Name.from_dict(obj.get("name"))
        pathway = Name.from_dict(obj.get("pathway"))
        rank = int(from_str(obj.get("rank")))
        geometry = Geometry.from_dict(obj.get("geometry"))
        parent_loc_class = from_str(obj.get("class"))
        sort = from_none(obj.get("sort"))
        score = from_int(obj.get("_score"))
        return ParentLOC(osm_id, parent_osm_id, level, subs, center, right, type, seo_title, depth, left, admin_level,
                         name, pathway, rank, geometry, parent_loc_class, sort, score)

    def to_dict(self) -> dict:
        result: dict = {}
        result["osm_id"] = from_int(self.osm_id)
        result["parent_osm_id"] = from_int(self.parent_osm_id)
        result["level"] = from_int(self.level)
        result["subs"] = from_int(self.subs)
        result["center"] = to_class(ParentLOCCenter, self.center)
        result["right"] = from_int(self.right)
        result["type"] = from_str(self.type)
        result["seo_title"] = to_class(Name, self.seo_title)
        result["depth"] = from_int(self.depth)
        result["left"] = from_int(self.left)
        result["admin_level"] = from_str(str(self.admin_level))
        result["name"] = to_class(Name, self.name)
        result["pathway"] = to_class(Name, self.pathway)
        result["rank"] = from_str(str(self.rank))
        result["geometry"] = to_class(Geometry, self.geometry)
        result["class"] = from_str(self.parent_loc_class)
        result["sort"] = from_none(self.sort)
        result["_score"] = from_int(self.score)
        return result


class PointCenter:
    lat: str
    lng: str

    def __init__(self, lat: str, lng: str) -> None:
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> 'PointCenter':
        assert isinstance(obj, dict)
        lat = from_str(obj.get("lat"))
        lng = from_str(obj.get("lng"))
        return PointCenter(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lat"] = from_str(self.lat)
        result["lng"] = from_str(self.lng)
        return result


OwnerType = str


class Currency(Enum):
    EMPTY = "₾"


class Price:
    amount: str
    currency: Currency

    def __init__(self, amount: str, currency: Currency) -> None:
        self.amount = amount
        self.currency = currency

    @staticmethod
    def from_dict(obj: Any) -> 'Price':
        assert isinstance(obj, dict)
        amount = from_str(obj.get("amount"))
        currency = Currency(obj.get("currency"))
        return Price(amount, currency)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_str(self.amount)
        result["currency"] = to_enum(Currency, self.currency)
        return result


Title = str


class Point:
    product_id: int
    found_by_id: int
    href: str
    price: Price
    center: PointCenter
    title: Title
    owner_type: OwnerType
    img: str
    avatar: str
    letter: str

    def __init__(self, product_id: int, found_by_id: int, href: str, price: Price, center: PointCenter, title: Title,
                 owner_type: OwnerType, img: str, avatar: str, letter: str) -> None:
        self.product_id = product_id
        self.found_by_id = found_by_id
        self.href = href
        self.price = price
        self.center = center
        self.title = title
        self.owner_type = owner_type
        self.img = img
        self.avatar = avatar
        self.letter = letter

    @staticmethod
    def from_dict(obj: Any) -> 'Point':
        assert isinstance(obj, dict)
        product_id = int(from_str(obj.get("product_id")))
        found_by_id = from_int(obj.get("FoundByID"))
        href = from_str(obj.get("href"))
        price = Price.from_dict(obj.get("price"))
        center = PointCenter.from_dict(obj.get("center"))
        title = Title(obj.get("title"))
        owner_type = OwnerType(obj.get("owner_type"))
        img = from_str(obj.get("img"))
        avatar = from_str(obj.get("avatar"))
        letter = from_str(obj.get("letter"))
        return Point(product_id, found_by_id, href, price, center, title, owner_type, img, avatar, letter)

    def to_dict(self) -> dict:
        result: dict = {}
        result["product_id"] = from_str(str(self.product_id))
        result["FoundByID"] = from_int(self.found_by_id)
        result["href"] = from_str(self.href)
        result["price"] = to_class(Price, self.price)
        result["center"] = to_class(PointCenter, self.center)
        result["title"] = self.title
        result["owner_type"] = self.owner_type
        result["img"] = from_str(self.img)
        result["avatar"] = from_str(self.avatar)
        result["letter"] = from_str(self.letter)
        return result


class MapData:
    parent_loc: ParentLOC
    points: List[Point]

    def __init__(self, parent_loc: ParentLOC, points: List[Point]) -> None:
        self.parent_loc = parent_loc
        self.points = points

    @staticmethod
    def from_dict(obj: Any) -> 'MapData':
        assert isinstance(obj, dict)
        parent_loc = ParentLOC.from_dict(obj.get("ParentLoc"))
        points = from_list(Point.from_dict, obj.get("Points"))
        return MapData(parent_loc, points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ParentLoc"] = to_class(ParentLOC, self.parent_loc)
        result["Points"] = from_list(lambda x: to_class(Point, x), self.points)
        return result


class Datum:
    user_id: int
    username: str
    gender_id: int
    personal_data_agreement: int
    agree_tbc_terms: int

    def __init__(self, user_id: int, username: str, gender_id: int, personal_data_agreement: int,
                 agree_tbc_terms: int) -> None:
        self.user_id = user_id
        self.username = username
        self.gender_id = gender_id
        self.personal_data_agreement = personal_data_agreement
        self.agree_tbc_terms = agree_tbc_terms

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        assert isinstance(obj, dict)
        user_id = int(from_str(obj.get("user_id")))
        username = from_str(obj.get("username"))
        gender_id = int(from_str(obj.get("gender_id")))
        personal_data_agreement = int(from_str(obj.get("personal_data_agreement")))
        agree_tbc_terms = int(from_str(obj.get("AgreeTBCTerms")))
        return Datum(user_id, username, gender_id, personal_data_agreement, agree_tbc_terms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user_id"] = from_str(str(self.user_id))
        result["username"] = from_str(self.username)
        result["gender_id"] = from_str(str(self.gender_id))
        result["personal_data_agreement"] = from_str(str(self.personal_data_agreement))
        result["AgreeTBCTerms"] = from_str(str(self.agree_tbc_terms))
        return result


class Users:
    status_code: int
    status_message: str
    data: Dict[str, Datum]

    def __init__(self, status_code: int, status_message: str, data: Dict[str, Datum]) -> None:
        self.status_code = status_code
        self.status_message = status_message
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'Users':
        assert isinstance(obj, dict)
        status_code = from_int(obj.get("StatusCode"))
        status_message = from_str(obj.get("StatusMessage"))
        data = from_dict(Datum.from_dict, obj.get("Data"))
        return Users(status_code, status_message, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["StatusCode"] = from_int(self.status_code)
        result["StatusMessage"] = from_str(self.status_message)
        result["Data"] = from_dict(lambda x: to_class(Datum, x), self.data)
        return result


class Product:
    product_id: int
    user_id: int
    parent_id: None
    makler_id: None
    has_logo: None
    makler_name: None
    loc_id: int
    street_address: str
    yard_size: int
    yard_size_type_id: int
    submission_id: None
    adtype_id: int
    product_type_id: int
    price: str
    photo: str
    photo_ver: int
    photos_count: int
    area_size_value: int
    video_url: str
    currency_id: int
    order_date: datetime
    price_type_id: int
    vip: int
    color: int
    estate_type_id: int
    area_size: str
    area_size_type_id: int
    comment: None
    map_lat: str
    map_lon: str
    l_living: int
    special_persons: int
    rooms: str
    bedrooms: int
    floor: int
    parking_id: int
    canalization: int
    water: int
    road: int
    electricity: int
    owner_type_id: int
    osm_id: int
    name_json: str
    pathway_json: str
    homeselfie: int
    seo_title_json: str
    seo_name_json: None

    def __init__(self, product_id: int, user_id: int, parent_id: None, makler_id: None, has_logo: None,
                 makler_name: None, loc_id: int, street_address: str, yard_size: int, yard_size_type_id: int,
                 submission_id: None, adtype_id: int, product_type_id: int, price: str, photo: str, photo_ver: int,
                 photos_count: int, area_size_value: int, video_url: str, currency_id: int, order_date: datetime,
                 price_type_id: int, vip: int, color: int, estate_type_id: int, area_size: str, area_size_type_id: int,
                 comment: None, map_lat: str, map_lon: str, l_living: int, special_persons: int, rooms: str,
                 bedrooms: int, floor: int, parking_id: int, canalization: int, water: int, road: int, electricity: int,
                 owner_type_id: int, osm_id: int, name_json: str, pathway_json: str, homeselfie: int,
                 seo_title_json: str, seo_name_json: None) -> None:
        self.product_id = product_id
        self.user_id = user_id
        self.parent_id = parent_id
        self.makler_id = makler_id
        self.has_logo = has_logo
        self.makler_name = makler_name
        self.loc_id = loc_id
        self.street_address = street_address
        self.yard_size = yard_size
        self.yard_size_type_id = yard_size_type_id
        self.submission_id = submission_id
        self.adtype_id = adtype_id
        self.product_type_id = product_type_id
        self.price = price
        self.photo = photo
        self.photo_ver = photo_ver
        self.photos_count = photos_count
        self.area_size_value = area_size_value
        self.video_url = video_url
        self.currency_id = currency_id
        self.order_date = order_date
        self.price_type_id = price_type_id
        self.vip = vip
        self.color = color
        self.estate_type_id = estate_type_id
        self.area_size = area_size
        self.area_size_type_id = area_size_type_id
        self.comment = comment
        self.map_lat = map_lat
        self.map_lon = map_lon
        self.l_living = l_living
        self.special_persons = special_persons
        self.rooms = rooms
        self.bedrooms = bedrooms
        self.floor = floor
        self.parking_id = parking_id
        self.canalization = canalization
        self.water = water
        self.road = road
        self.electricity = electricity
        self.owner_type_id = owner_type_id
        self.osm_id = osm_id
        self.name_json = name_json
        self.pathway_json = pathway_json
        self.homeselfie = homeselfie
        self.seo_title_json = seo_title_json
        self.seo_name_json = seo_name_json

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        assert isinstance(obj, dict)
        product_id = int(from_str(obj.get("product_id")))
        user_id = int(from_str(obj.get("user_id")))
        parent_id = from_none(obj.get("parent_id"))
        makler_id = from_none(obj.get("makler_id"))
        has_logo = from_none(obj.get("has_logo"))
        makler_name = from_none(obj.get("makler_name"))
        loc_id = int(from_str(obj.get("loc_id")))
        street_address = from_str(obj.get("street_address"))
        yard_size = int(from_str(obj.get("yard_size")))
        yard_size_type_id = int(from_str(obj.get("yard_size_type_id")))
        submission_id = from_none(obj.get("submission_id"))
        adtype_id = int(from_str(obj.get("adtype_id")))
        product_type_id = int(from_str(obj.get("product_type_id")))
        price = from_str(obj.get("price"))
        photo = from_str(obj.get("photo"))
        photo_ver = int(from_str(obj.get("photo_ver")))
        photos_count = int(from_str(obj.get("photos_count")))
        area_size_value = int(from_str(obj.get("area_size_value")))
        video_url = from_str(obj.get("video_url"))
        currency_id = int(from_str(obj.get("currency_id")))
        order_date = from_datetime(obj.get("order_date"))
        price_type_id = int(from_str(obj.get("price_type_id")))
        vip = int(from_str(obj.get("vip")))
        color = int(from_str(obj.get("color")))
        estate_type_id = int(from_str(obj.get("estate_type_id")))
        area_size = from_str(obj.get("area_size"))
        area_size_type_id = int(from_str(obj.get("area_size_type_id")))
        comment = from_none(obj.get("comment"))
        map_lat = from_str(obj.get("map_lat"))
        map_lon = from_str(obj.get("map_lon"))
        l_living = int(from_str(obj.get("l_living")))
        special_persons = int(from_str(obj.get("special_persons")))
        rooms = from_str(obj.get("rooms"))
        bedrooms = int(from_str(obj.get("bedrooms")))
        floor = int(from_str(obj.get("floor")))
        parking_id = int(from_str(obj.get("parking_id")))
        canalization = int(from_str(obj.get("canalization")))
        water = int(from_str(obj.get("water")))
        road = int(from_str(obj.get("road")))
        electricity = int(from_str(obj.get("electricity")))
        owner_type_id = int(from_str(obj.get("owner_type_id")))
        osm_id = int(from_str(obj.get("osm_id")))
        name_json = from_str(obj.get("name_json"))
        pathway_json = from_str(obj.get("pathway_json"))
        homeselfie = int(from_str(obj.get("homeselfie")))
        seo_title_json = from_str(obj.get("seo_title_json"))
        seo_name_json = from_none(obj.get("seo_name_json"))
        return Product(product_id, user_id, parent_id, makler_id, has_logo, makler_name, loc_id, street_address,
                       yard_size, yard_size_type_id, submission_id, adtype_id, product_type_id, price, photo,
                       photo_ver, photos_count, area_size_value, video_url, currency_id, order_date, price_type_id,
                       vip, color, estate_type_id, area_size, area_size_type_id, comment, map_lat, map_lon, l_living,
                       special_persons, rooms, bedrooms, floor, parking_id, canalization, water, road, electricity,
                       owner_type_id, osm_id, name_json, pathway_json, homeselfie, seo_title_json, seo_name_json)

    def to_dict(self) -> dict:
        result: dict = {}
        result["product_id"] = from_str(str(self.product_id))
        result["user_id"] = from_str(str(self.user_id))
        result["parent_id"] = from_none(self.parent_id)
        result["makler_id"] = from_none(self.makler_id)
        result["has_logo"] = from_none(self.has_logo)
        result["makler_name"] = from_none(self.makler_name)
        result["loc_id"] = from_str(str(self.loc_id))
        result["street_address"] = from_str(self.street_address)
        result["yard_size"] = from_str(str(self.yard_size))
        result["yard_size_type_id"] = from_str(str(self.yard_size_type_id))
        result["submission_id"] = from_none(self.submission_id)
        result["adtype_id"] = from_str(str(self.adtype_id))
        result["product_type_id"] = from_str(str(self.product_type_id))
        result["price"] = from_str(self.price)
        result["photo"] = from_str(self.photo)
        result["photo_ver"] = from_str(str(self.photo_ver))
        result["photos_count"] = from_str(str(self.photos_count))
        result["area_size_value"] = from_str(str(self.area_size_value))
        result["video_url"] = from_str(self.video_url)
        result["currency_id"] = from_str(str(self.currency_id))
        result["order_date"] = self.order_date.isoformat()
        result["price_type_id"] = from_str(str(self.price_type_id))
        result["vip"] = from_str(str(self.vip))
        result["color"] = from_str(str(self.color))
        result["estate_type_id"] = from_str(str(self.estate_type_id))
        result["area_size"] = from_str(self.area_size)
        result["area_size_type_id"] = from_str(str(self.area_size_type_id))
        result["comment"] = from_none(self.comment)
        result["map_lat"] = from_str(self.map_lat)
        result["map_lon"] = from_str(self.map_lon)
        result["l_living"] = from_str(str(self.l_living))
        result["special_persons"] = from_str(str(self.special_persons))
        result["rooms"] = from_str(self.rooms)
        result["bedrooms"] = from_str(str(self.bedrooms))
        result["floor"] = from_str(str(self.floor))
        result["parking_id"] = from_str(str(self.parking_id))
        result["canalization"] = from_str(str(self.canalization))
        result["water"] = from_str(str(self.water))
        result["road"] = from_str(str(self.road))
        result["electricity"] = from_str(str(self.electricity))
        result["owner_type_id"] = from_str(str(self.owner_type_id))
        result["osm_id"] = from_str(str(self.osm_id))
        result["name_json"] = from_str(self.name_json)
        result["pathway_json"] = from_str(self.pathway_json)
        result["homeselfie"] = from_str(str(self.homeselfie))
        result["seo_title_json"] = from_str(self.seo_title_json)
        result["seo_name_json"] = from_none(self.seo_name_json)
        return result


class Data:
    maklers: List[Any]
    prs: List[Product]
    floors: Dict[str, List[Floor]]
    users: Users
    cnt: int
    page: int
    filtered: bool
    map_data: MapData
    districts: Districts
    filter: str
    as_banner_locs_check: bool
    a2_reg_banner_locs_check: bool
    as_banner_show: bool
    typeform_qs: int

    def __init__(self, maklers: List[Any], prs: List[Dict[Product, Optional[Product]]], floors: Dict[str, List[Floor]],
                 users: Users, cnt: int, page: int, filtered: bool, map_data: MapData, districts: Districts,
                 filter: str, as_banner_locs_check: bool, a2_reg_banner_locs_check: bool, as_banner_show: bool,
                 typeform_qs: int) -> None:
        self.maklers = maklers
        self.prs = prs
        self.floors = floors
        self.users = users
        self.cnt = cnt
        self.page = page
        self.filtered = filtered
        self.map_data = map_data
        self.districts = districts
        self.filter = filter
        self.as_banner_locs_check = as_banner_locs_check
        self.a2_reg_banner_locs_check = a2_reg_banner_locs_check
        self.as_banner_show = as_banner_show
        self.typeform_qs = typeform_qs

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        maklers = from_list(lambda x: x, obj.get("Maklers"))
        prs = [Product.from_dict(j) for j in obj.get("Prs")]
        floors = from_dict(lambda x: from_list(Floor.from_dict, x), obj.get("Floors"))
        users = Users.from_dict(obj.get("Users"))
        cnt = int(from_str(obj.get("Cnt")))
        page = from_int(obj.get("Page"))
        filtered = from_bool(obj.get("Filtered"))
        map_data = MapData.from_dict(obj.get("MapData"))
        districts = Districts.from_dict(obj.get("Districts"))
        filter = from_str(obj.get("filter"))
        as_banner_locs_check = from_bool(obj.get("ASBannerLocsCheck"))
        a2_reg_banner_locs_check = from_bool(obj.get("A2RegBannerLocsCheck"))
        as_banner_show = from_bool(obj.get("ASBannerShow"))
        typeform_qs = from_int(obj.get("typeformQs"))
        return Data(maklers, prs, floors, users, cnt, page, filtered, map_data, districts, filter, as_banner_locs_check,
                    a2_reg_banner_locs_check, as_banner_show, typeform_qs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Maklers"] = from_list(lambda x: x, self.maklers)
        result["Prs"] = from_list(lambda x: from_dict(lambda x: from_union([from_none, from_str], x), x), self.prs)
        result["Floors"] = from_dict(lambda x: from_list(lambda x: to_class(Floor, x), x), self.floors)
        result["Users"] = to_class(Users, self.users)
        result["Cnt"] = from_str(str(self.cnt))
        result["Page"] = from_int(self.page)
        result["Filtered"] = from_bool(self.filtered)
        result["MapData"] = to_class(MapData, self.map_data)
        result["Districts"] = to_class(Districts, self.districts)
        result["filter"] = from_str(self.filter)
        result["ASBannerLocsCheck"] = from_bool(self.as_banner_locs_check)
        result["A2RegBannerLocsCheck"] = from_bool(self.a2_reg_banner_locs_check)
        result["ASBannerShow"] = from_bool(self.as_banner_show)
        result["typeformQs"] = from_int(self.typeform_qs)
        return result


class Response:
    status_code: int
    status_message: str
    data: Data

    def __init__(self, status_code: int, status_message: str, data: Data) -> None:
        self.status_code = status_code
        self.status_message = status_message
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'Response':
        assert isinstance(obj, dict)
        status_code = from_int(obj.get("StatusCode"))
        status_message = from_str(obj.get("StatusMessage"))
        data = Data.from_dict(obj.get("Data"))
        return Response(status_code, status_message, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["StatusCode"] = from_int(self.status_code)
        result["StatusMessage"] = from_str(self.status_message)
        result["Data"] = to_class(Data, self.data)
        return result