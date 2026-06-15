from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI(title="Music Mood Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoodRequest(BaseModel):
    mood: str        # 행복, 우울, 설렘, 피곤, 집중
    activity: str    # 공부, 운동, 드라이브, 휴식, 작업
    tempo: str       # 느림, 보통, 빠름
    genre: str       # K-Pop, J-Pop, Pop, R&B, 인디

class Song(BaseModel):
    title: str
    artist: str
    genre: str
    reason: str

class RecommendResponse(BaseModel):
    playlist_name: str
    description: str
    genre_tag: str
    songs: List[Song]

# ── 장르별 곡 데이터베이스 ──────────────────────────────────────
SONG_DB = {
    # (mood, tempo, genre) → songs

    # ── 행복 ──────────────────────────────────────────────────
    ("행복", "빠름", "K-Pop"): [
        Song(title="Dynamite", artist="BTS", genre="K-Pop", reason="밝고 신나는 에너지로 기분을 더욱 업시켜줘요"),
        Song(title="LOVE DIVE", artist="IVE", genre="K-Pop", reason="경쾌한 리듬이 행복한 순간을 완성해줘요"),
        Song(title="Ditto", artist="NewJeans", genre="K-Pop", reason="설레는 감정을 담은 감각적인 사운드"),
        Song(title="TOMBOY", artist="(G)I-DLE", genre="K-Pop", reason="자신감 넘치는 비트로 에너지 충전"),
        Song(title="Next Level", artist="aespa", genre="K-Pop", reason="강렬하고 신나는 사운드로 기분 UP"),
    ],
    ("행복", "빠름", "J-Pop"): [
        Song(title="Pretender", artist="Official髭男dism", genre="J-Pop", reason="일본 특유의 감성적인 업비트"),
        Song(title="香水", artist="瑛人", genre="J-Pop", reason="달콤하고 산뜻한 멜로디"),
        Song(title="夜に駆ける", artist="YOASOBI", genre="J-Pop", reason="빠른 템포로 달리는 듯한 에너지"),
        Song(title="ドライフラワー", artist="優里", genre="J-Pop", reason="감성적인 행복을 담은 곡"),
        Song(title="Paprika", artist="米津玄師", genre="J-Pop", reason="밝고 동화 같은 분위기"),
    ],
    ("행복", "빠름", "Pop"): [
        Song(title="Can't Stop the Feeling", artist="Justin Timberlake", genre="Pop", reason="몸이 저절로 움직이는 신나는 리듬"),
        Song(title="Uptown Funk", artist="Mark Ronson ft. Bruno Mars", genre="Pop/Funk", reason="중독성 있는 비트로 기분 최고"),
        Song(title="Shake It Off", artist="Taylor Swift", genre="Pop", reason="긍정 에너지 폭발하는 곡"),
        Song(title="Happy", artist="Pharrell Williams", genre="Pop/Soul", reason="행복 그 자체를 담은 곡"),
        Song(title="Good as Hell", artist="Lizzo", genre="Pop", reason="자존감을 높여주는 신나는 곡"),
    ],
    ("행복", "빠름", "R&B"): [
        Song(title="Watermelon Sugar", artist="Harry Styles", genre="Pop/R&B", reason="여름처럼 달콤하고 신나는 곡"),
        Song(title="Leave The Door Open", artist="Bruno Mars & Anderson .Paak", genre="R&B/Soul", reason="세련되고 행복한 소울 바이브"),
        Song(title="Essence", artist="Wizkid ft. Tems", genre="Afrobeats/R&B", reason="그루비하고 신나는 에너지"),
        Song(title="Don't Start Now", artist="Dua Lipa", genre="Dance/R&B", reason="강렬하게 신나는 댄스 R&B"),
        Song(title="Levitating", artist="Dua Lipa", genre="Pop/R&B", reason="둥실 떠오르는 행복한 느낌"),
    ],
    ("행복", "빠름", "인디"): [
        Song(title="Electric Love", artist="BØRNS", genre="인디팝", reason="전기처럼 짜릿한 에너지"),
        Song(title="Little Talks", artist="Of Monsters and Men", genre="인디포크", reason="신나고 따뜻한 인디 바이브"),
        Song(title="Do I Wanna Know?", artist="Arctic Monkeys", genre="인디록", reason="강렬하고 쿨한 리듬"),
        Song(title="Mr. Brightside", artist="The Killers", genre="인디록", reason="달리게 만드는 전설적인 곡"),
        Song(title="Take Me Out", artist="Franz Ferdinand", genre="인디록", reason="에너지 넘치는 인디록"),
    ],
    ("행복", "보통", "K-Pop"): [
        Song(title="Celebrity", artist="IU", genre="K-Pop", reason="따뜻하고 사랑스러운 분위기"),
        Song(title="Hype boy", artist="NewJeans", genre="K-Pop", reason="청량하고 사랑스러운 사운드"),
        Song(title="라일락", artist="IU", genre="K-Pop", reason="봄처럼 따뜻하고 기분 좋은 멜로디"),
        Song(title="ANTIFRAGILE", artist="LE SSERAFIM", genre="K-Pop", reason="자신감과 행복이 담긴 곡"),
        Song(title="ELEVEN", artist="IVE", genre="K-Pop", reason="설레는 감정을 담은 발랄한 곡"),
    ],
    ("행복", "보통", "J-Pop"): [
        Song(title="パプリカ", artist="Foorin", genre="J-Pop", reason="밝고 신나는 어린이날 같은 에너지"),
        Song(title="明日も", artist="YOASOBI", genre="J-Pop", reason="밝은 내일을 향한 설레는 곡"),
        Song(title="Lemon", artist="米津玄師", genre="J-Pop", reason="달콤하면서 감성적인 명곡"),
        Song(title="マリーゴールド", artist="あいみょん", genre="J-Pop", reason="따뜻한 햇살 같은 분위기"),
        Song(title="なんでもないや", artist="RADWIMPS", genre="J-Pop/Rock", reason="청춘의 행복을 담은 곡"),
    ],
    ("행복", "보통", "Pop"): [
        Song(title="Sunflower", artist="Post Malone & Swae Lee", genre="Pop", reason="따뜻하고 기분 좋은 바이브"),
        Song(title="golden hour", artist="JVKE", genre="Pop", reason="황금빛 오후 같은 따뜻한 곡"),
        Song(title="Blinding Lights", artist="The Weeknd", genre="신스팝", reason="신나면서도 감성적인 느낌"),
        Song(title="As It Was", artist="Harry Styles", genre="Pop", reason="경쾌하고 감성적인 명곡"),
        Song(title="Lover", artist="Taylor Swift", genre="Pop", reason="사랑스럽고 행복한 감성"),
    ],
    ("행복", "보통", "R&B"): [
        Song(title="No Air", artist="Jordin Sparks & Chris Brown", genre="R&B/Pop", reason="달콤하고 행복한 사랑의 느낌"),
        Song(title="Golden", artist="Harry Styles", genre="Pop/R&B", reason="황금빛처럼 반짝이는 행복"),
        Song(title="Peaches", artist="Justin Bieber ft. Daniel Caesar", genre="R&B", reason="복숭아처럼 달콤한 여름 바이브"),
        Song(title="Girl Like You", artist="Maroon 5", genre="Pop/R&B", reason="사랑스럽고 신나는 바이브"),
        Song(title="24K Magic", artist="Bruno Mars", genre="Pop/R&B", reason="화려하고 신나는 파티 바이브"),
    ],
    ("행복", "보통", "인디"): [
        Song(title="Home", artist="Edward Sharpe and the Magnetic Zeros", genre="인디포크", reason="따뜻하고 행복한 집의 느낌"),
        Song(title="I'm Yours", artist="Jason Mraz", genre="인디팝", reason="여유롭고 행복한 바이브"),
        Song(title="Steal My Girl", artist="One Direction", genre="팝/인디", reason="사랑스럽고 신나는 곡"),
        Song(title="Riptide", artist="Vance Joy", genre="인디팝", reason="청량하고 행복한 감성"),
        Song(title="Ho Hey", artist="The Lumineers", genre="인디포크", reason="신나는 인디포크 명곡"),
    ],
    ("행복", "느림", "K-Pop"): [
        Song(title="밤편지", artist="IU", genre="K-Pop/인디", reason="포근하고 행복한 감성"),
        Song(title="좋은 날", artist="IU", genre="K-Pop", reason="맑고 행복한 목소리"),
        Song(title="봄날", artist="BTS", genre="K-Pop", reason="아름다운 감성의 명곡"),
        Song(title="한 페이지가 될 수 있게", artist="DAY6", genre="K-Pop/Rock", reason="감동적이고 따뜻한 곡"),
        Song(title="Through the Night", artist="IU", genre="K-Pop", reason="밤을 함께하는 따뜻한 곡"),
    ],
    ("행복", "느림", "J-Pop"): [
        Song(title="愛燦燦", artist="美空ひばり", genre="J-Pop/演歌", reason="오래된 명곡의 따뜻한 감동"),
        Song(title="三日月", artist="絢香", genre="J-Pop", reason="달빛처럼 포근한 행복"),
        Song(title="キセキ", artist="GReeeeN", genre="J-Pop", reason="기적 같은 행복을 담은 명곡"),
        Song(title="First Love", artist="宇多田ヒカル", genre="J-Pop/R&B", reason="첫사랑처럼 순수하고 따뜻한 곡"),
        Song(title="Jupiter", artist="平原綾香", genre="J-Pop", reason="웅장하고 감동적인 행복"),
    ],
    ("행복", "느림", "Pop"): [
        Song(title="Perfect", artist="Ed Sheeran", genre="Pop", reason="사랑스러운 감성의 명곡"),
        Song(title="A Thousand Years", artist="Christina Perri", genre="Pop", reason="영원한 사랑을 담은 곡"),
        Song(title="Make You Feel My Love", artist="Adele", genre="Pop", reason="깊고 따뜻한 감성"),
        Song(title="The Night We Met", artist="Lord Huron", genre="인디팝", reason="아름다운 감성의 곡"),
        Song(title="All of Me", artist="John Legend", genre="R&B/Pop", reason="온전한 사랑을 담은 명곡"),
    ],
    ("행복", "느림", "R&B"): [
        Song(title="Adorn", artist="Miguel", genre="R&B", reason="부드럽고 달콤한 사랑의 R&B"),
        Song(title="Best Part", artist="Daniel Caesar ft. H.E.R.", genre="R&B/Soul", reason="행복한 사랑을 담은 감미로운 곡"),
        Song(title="Die With A Smile", artist="Lady Gaga & Bruno Mars", genre="Pop/R&B", reason="아름답고 감동적인 사랑 노래"),
        Song(title="Slow Dance", artist="AJ Mitchell ft. Ava Max", genre="Pop/R&B", reason="느린 댄스처럼 달콤한 행복"),
        Song(title="Gravity", artist="John Mayer", genre="R&B/블루스", reason="깊고 감성적인 행복"),
    ],
    ("행복", "느림", "인디"): [
        Song(title="Skinny Love", artist="Bon Iver", genre="인디포크", reason="아련하면서 따뜻한 행복"),
        Song(title="Holocene", artist="Bon Iver", genre="인디포크", reason="광활한 자연 속 행복한 감성"),
        Song(title="Dog Days Are Over", artist="Florence + The Machine", genre="인디록", reason="지나간 힘든 날들 뒤의 행복"),
        Song(title="Such Great Heights", artist="The Postal Service", genre="인디팝", reason="높은 곳에서 내려다보는 행복"),
        Song(title="On Top of the World", artist="Imagine Dragons", genre="인디록", reason="세상 위에 있는 듯한 행복"),
    ],

    # ── 우울 ──────────────────────────────────────────────────
    ("우울", "느림", "K-Pop"): [
        Song(title="이런 엔딩", artist="Standing Egg", genre="K-Pop/인디", reason="공감되는 감성으로 위로를 줘요"),
        Song(title="나에게로 떠나는 여행", artist="자이언티", genre="K-Pop/R&B", reason="부드럽게 감정을 어루만지는 곡"),
        Song(title="무릎", artist="IU", genre="K-Pop", reason="담담하게 슬픔을 담은 곡"),
        Song(title="애월에서", artist="오왠", genre="K-Pop/인디", reason="잔잔하게 마음을 달래주는 곡"),
        Song(title="늦은 밤 너에게", artist="어반자카파", genre="K-Pop/R&B", reason="따뜻하게 감싸주는 목소리"),
    ],
    ("우울", "느림", "J-Pop"): [
        Song(title="花束みたいな恋をした", artist="YOASOBI", genre="J-Pop", reason="꽃다발 같은 사랑의 아련한 기억"),
        Song(title="残酷な天使のテーゼ", artist="高橋洋子", genre="J-Pop/애니", reason="감성적인 명곡의 위로"),
        Song(title="糸", artist="中島みゆき", genre="J-Pop", reason="인연을 담은 깊은 감성의 곡"),
        Song(title="366日", artist="HY", genre="J-Pop", reason="그리움과 슬픔을 담은 명곡"),
        Song(title="Hello, Again", artist="MY LITTLE LOVER", genre="J-Pop", reason="다시 만남을 꿈꾸는 아련한 곡"),
    ],
    ("우울", "느림", "Pop"): [
        Song(title="Someone Like You", artist="Adele", genre="Pop/Soul", reason="감정을 쏟아내게 해주는 명곡"),
        Song(title="Skinny Love", artist="Bon Iver", genre="인디포크", reason="날 것의 감성으로 공감을 주는 곡"),
        Song(title="Liability", artist="Lorde", genre="인디팝", reason="고독한 감정을 담담하게 담은 곡"),
        Song(title="drivers license", artist="Olivia Rodrigo", genre="Pop", reason="이별의 감정을 섬세하게 표현"),
        Song(title="Fix You", artist="Coldplay", genre="얼터너티브록", reason="슬픔을 치유하는 위로의 곡"),
    ],
    ("우울", "느림", "R&B"): [
        Song(title="Broken-Hearted Girl", artist="Beyoncé", genre="R&B/Pop", reason="상처받은 마음을 대변하는 곡"),
        Song(title="Love On The Brain", artist="Rihanna", genre="R&B/Soul", reason="강렬한 감정을 담은 곡"),
        Song(title="Heather", artist="Conan Gray", genre="인디팝/R&B", reason="섬세한 감정을 담은 아름다운 곡"),
        Song(title="Liability", artist="Lorde", genre="R&B/인디", reason="고독한 감정의 담담한 표현"),
        Song(title="Issues", artist="Julia Michaels", genre="Pop/R&B", reason="복잡한 감정을 솔직하게 담은 곡"),
    ],
    ("우울", "느림", "인디"): [
        Song(title="The Night We Met", artist="Lord Huron", genre="인디팝", reason="그리움과 슬픔을 담은 아름다운 곡"),
        Song(title="Re: Stacks", artist="Bon Iver", genre="인디포크", reason="지친 마음을 달래주는 곡"),
        Song(title="Lua", artist="Bright Eyes", genre="인디포크", reason="날 것의 고독한 감성"),
        Song(title="Skinny Love", artist="Bon Iver", genre="인디포크", reason="아련하고 슬픈 감성"),
        Song(title="Death With Dignity", artist="Sufjan Stevens", genre="인디포크", reason="깊은 슬픔을 담은 명곡"),
    ],
    ("우울", "보통", "K-Pop"): [
        Song(title="주저하는 연인들을 위해", artist="잔나비", genre="K-Pop/인디", reason="공감되는 감성의 명곡"),
        Song(title="오늘도 빛나는 너에게", artist="BTS", genre="K-Pop", reason="따뜻한 위로의 메시지"),
        Song(title="봄날", artist="BTS", genre="K-Pop", reason="긴 터널 끝의 빛 같은 곡"),
        Song(title="잊어야 한다는 걸", artist="정승환", genre="K-Pop/발라드", reason="이별의 아픔을 아름답게 표현"),
        Song(title="팔레트", artist="IU", genre="K-Pop", reason="담담하게 나를 돌아보는 곡"),
    ],
    ("우울", "보통", "J-Pop"): [
        Song(title="群青", artist="YOASOBI", genre="J-Pop", reason="파란 하늘처럼 감성적인 위로"),
        Song(title="ありがとう", artist="いきものがかり", genre="J-Pop", reason="고마움을 담은 따뜻한 위로"),
        Song(title="にじいろ", artist="絢香", genre="J-Pop", reason="무지개처럼 다양한 감정을 담은 곡"),
        Song(title="サウダージ", artist="ポルノグラフィティ", genre="J-Pop/Rock", reason="그리움을 담은 명곡"),
        Song(title="虹", artist="菅田将暉", genre="J-Pop", reason="비 온 뒤 무지개 같은 감동"),
    ],
    ("우울", "보통", "Pop"): [
        Song(title="lovely", artist="Billie Eilish & Khalid", genre="Pop", reason="아름답고 슬픈 감성"),
        Song(title="Happier", artist="Olivia Rodrigo", genre="Pop", reason="공감되는 이별 감성"),
        Song(title="Let Her Go", artist="Passenger", genre="포크팝", reason="잃고 나서야 아는 소중함"),
        Song(title="Easy On Me", artist="Adele", genre="Pop", reason="부드럽게 감싸주는 곡"),
        Song(title="The 1", artist="Taylor Swift", genre="인디팝", reason="아련하고 슬픈 감성"),
    ],
    ("우울", "보통", "R&B"): [
        Song(title="Earned It", artist="The Weeknd", genre="R&B", reason="복잡한 감정을 담은 감성적인 곡"),
        Song(title="The Hills", artist="The Weeknd", genre="R&B", reason="어두운 감성의 R&B 명곡"),
        Song(title="Call Out My Name", artist="The Weeknd", genre="R&B", reason="이별의 아픔을 담은 곡"),
        Song(title="I Fall Apart", artist="Post Malone", genre="Pop/R&B", reason="무너지는 감정을 솔직하게 담은 곡"),
        Song(title="Location", artist="Khalid", genre="R&B", reason="쓸쓸하지만 감성적인 R&B"),
    ],
    ("우울", "보통", "인디"): [
        Song(title="Flightless Bird", artist="Iron & Wine", genre="인디포크", reason="날지 못하는 새처럼 아련한 감성"),
        Song(title="Holocene", artist="Bon Iver", genre="인디포크", reason="광활한 외로움을 담은 명곡"),
        Song(title="Motion Picture Soundtrack", artist="Radiohead", genre="얼터너티브/인디", reason="영화 속 한 장면 같은 슬픔"),
        Song(title="Lua", artist="Bright Eyes", genre="인디포크", reason="고독한 감성의 인디 명곡"),
        Song(title="From Eden", artist="Hozier", genre="인디록/포크", reason="아름답고 슬픈 감성"),
    ],
    ("우울", "빠름", "K-Pop"): [
        Song(title="파이팅 해야지", artist="(여자)아이들", genre="K-Pop", reason="우울할 때 힘을 주는 곡"),
        Song(title="Rollin'", artist="브레이브걸스", genre="K-Pop", reason="기분 전환에 딱 좋은 신나는 곡"),
        Song(title="Weekend", artist="태연", genre="K-Pop", reason="일상 탈출을 꿈꾸는 경쾌한 곡"),
        Song(title="DALLA DALLA", artist="ITZY", genre="K-Pop", reason="자신감 넘치는 에너지"),
        Song(title="음오아예", artist="f(x)", genre="K-Pop", reason="독특한 에너지로 기분 UP"),
    ],
    ("우울", "빠름", "J-Pop"): [
        Song(title="ハッピーエンド", artist="back number", genre="J-Pop", reason="해피엔딩을 바라는 에너지"),
        Song(title="サビだけ", artist="あいみょん", genre="J-Pop", reason="빠르고 감성적인 위로"),
        Song(title="ロキ", artist="まふまふ", genre="J-Pop/보카로", reason="강렬하게 감정을 발산하는 곡"),
        Song(title="紅蓮華", artist="LiSA", genre="J-Pop/애니", reason="역경을 이겨내는 강한 에너지"),
        Song(title="Pretender", artist="Official髭男dism", genre="J-Pop", reason="빠른 템포의 감성적인 위로"),
    ],
    ("우울", "빠름", "Pop"): [
        Song(title="Shake It Off", artist="Taylor Swift", genre="Pop", reason="부정적인 감정을 털어버리는 곡"),
        Song(title="Good as Hell", artist="Lizzo", genre="Pop/R&B", reason="자존감을 회복시켜주는 곡"),
        Song(title="Fight Song", artist="Rachel Platten", genre="Pop", reason="용기를 주는 응원가"),
        Song(title="Confident", artist="Demi Lovato", genre="팝록", reason="자신감을 불어넣어주는 곡"),
        Song(title="Stronger", artist="Kelly Clarkson", genre="팝록", reason="역경을 이겨내는 메시지"),
    ],
    ("우울", "빠름", "R&B"): [
        Song(title="Formation", artist="Beyoncé", genre="R&B/Hip-Hop", reason="자신감 폭발하는 강렬한 곡"),
        Song(title="Sorry Not Sorry", artist="Demi Lovato", genre="Pop/R&B", reason="당당하게 감정을 표현하는 곡"),
        Song(title="Run the World (Girls)", artist="Beyoncé", genre="R&B/Pop", reason="자존감을 높여주는 명곡"),
        Song(title="Irreplaceable", artist="Beyoncé", genre="R&B/Pop", reason="당당한 이별을 담은 명곡"),
        Song(title="Needed Me", artist="Rihanna", genre="R&B", reason="강렬하게 감정을 털어내는 곡"),
    ],
    ("우울", "빠름", "인디"): [
        Song(title="Dog Days Are Over", artist="Florence + The Machine", genre="인디록", reason="힘든 날이 지나간다는 희망"),
        Song(title="Ready to Run", artist="One Direction", genre="팝/인디", reason="달리고 싶어지는 에너지"),
        Song(title="Pumped Up Kicks", artist="Foster the People", genre="인디팝", reason="경쾌한 리듬으로 기분 전환"),
        Song(title="Stubborn Love", artist="The Lumineers", genre="인디포크", reason="고집스러운 사랑의 에너지"),
        Song(title="Sprawl II", artist="Arcade Fire", genre="인디팝", reason="탈출하고 싶은 감정을 담은 곡"),
    ],

    # ── 설렘 ──────────────────────────────────────────────────
    ("설렘", "빠름", "K-Pop"): [
        Song(title="Hype boy", artist="NewJeans", genre="K-Pop", reason="설레는 감정을 완벽하게 담은 곡"),
        Song(title="OMG", artist="NewJeans", genre="K-Pop", reason="두근두근한 첫 만남의 감성"),
        Song(title="ELEVEN", artist="IVE", genre="K-Pop", reason="첫사랑의 설렘을 담은 곡"),
        Song(title="FEARLESS", artist="LE SSERAFIM", genre="K-Pop", reason="당당하고 설레는 에너지"),
        Song(title="애플", artist="지코", genre="K-Pop/Hip-Hop", reason="강렬하게 빠져드는 설렘"),
    ],
    ("설렘", "빠름", "J-Pop"): [
        Song(title="恋", artist="星野源", genre="J-Pop", reason="사랑에 빠지는 설레는 감성"),
        Song(title="Love music", artist="フジファブリック", genre="J-Pop", reason="사랑의 음악처럼 설레는 곡"),
        Song(title="告白日和", artist="back number", genre="J-Pop", reason="고백하는 날처럼 두근두근"),
        Song(title="僕が君の名前を呼んだ日", artist="SEKAI NO OWARI", genre="J-Pop", reason="이름을 부르는 순간의 설렘"),
        Song(title="LOVEずっきゅん", artist="でんぱ組.inc", genre="J-Pop/아이돌", reason="큐피드 화살처럼 쏘는 설렘"),
    ],
    ("설렘", "빠름", "Pop"): [
        Song(title="Love Story", artist="Taylor Swift", genre="Pop/Country", reason="동화 같은 설레는 사랑 이야기"),
        Song(title="Electric Love", artist="BØRNS", genre="인디팝", reason="전기처럼 짜릿한 설렘"),
        Song(title="Sparks Fly", artist="Taylor Swift", genre="Pop", reason="불꽃처럼 튀는 설렘"),
        Song(title="Enchanted", artist="Taylor Swift", genre="Pop", reason="마법 같은 첫 만남의 감성"),
        Song(title="Crush", artist="Jennifer Paige", genre="Pop", reason="첫사랑의 두근거림"),
    ],
    ("설렘", "빠름", "R&B"): [
        Song(title="Thinking Out Loud", artist="Ed Sheeran", genre="Pop/R&B", reason="춤추고 싶은 설레는 사랑"),
        Song(title="Earned It", artist="The Weeknd", genre="R&B", reason="빠져들게 만드는 강렬한 설렘"),
        Song(title="Positions", artist="Ariana Grande", genre="Pop/R&B", reason="달콤하고 설레는 감성"),
        Song(title="Wildest Dreams", artist="Taylor Swift", genre="팝/R&B", reason="꿈속 같은 설레는 감성"),
        Song(title="Die For You", artist="The Weeknd", genre="R&B", reason="강렬하게 빠져드는 사랑"),
    ],
    ("설렘", "빠름", "인디"): [
        Song(title="Take Me to Church", artist="Hozier", genre="인디록/소울", reason="강렬하게 빠져드는 설렘"),
        Song(title="Cecilia and the Satellite", artist="Andrew McMahon", genre="인디팝", reason="반짝이는 설레는 감성"),
        Song(title="The Less I Know the Better", artist="Tame Impala", genre="사이키델릭록/인디", reason="빠져드는 몽환적인 설렘"),
        Song(title="Tongue Tied", artist="Grouplove", genre="인디록", reason="말문이 막히는 설렘"),
        Song(title="Stolen Dance", artist="Milky Chance", genre="인디팝", reason="훔쳐간 춤처럼 달콤한 설렘"),
    ],
    ("설렘", "보통", "K-Pop"): [
        Song(title="봄봄봄", artist="로이킴", genre="K-Pop/포크", reason="봄처럼 설레는 감성"),
        Song(title="사랑에 빠져요", artist="볼빨간사춘기", genre="K-Pop/인디", reason="달달한 사랑의 설렘"),
        Song(title="썸", artist="소유 & 정기고", genre="K-Pop/R&B", reason="설레는 '썸' 타는 감성"),
        Song(title="우주를 줄게", artist="볼빨간사춘기", genre="K-Pop/인디", reason="순수하고 달콤한 사랑"),
        Song(title="Blue Flame", artist="SF9", genre="K-Pop", reason="산뜻하고 설레는 사운드"),
    ],
    ("설렘", "보통", "J-Pop"): [
        Song(title="恋人よ", artist="五輪真弓", genre="J-Pop", reason="연인에게 전하는 설레는 마음"),
        Song(title="プリズム", artist="ゆず", genre="J-Pop", reason="프리즘처럼 빛나는 설렘"),
        Song(title="恋", artist="星野源", genre="J-Pop", reason="사랑에 빠지는 설레는 감성"),
        Song(title="愛を伝えたいだとか", artist="あいみょん", genre="J-Pop", reason="사랑을 전하고 싶은 설레는 마음"),
        Song(title="春風", artist="STUTS & 松たか子", genre="J-Pop", reason="봄바람처럼 산들산들한 설렘"),
    ],
    ("설렘", "보통", "Pop"): [
        Song(title="golden hour", artist="JVKE", genre="Pop", reason="황금빛 설렘을 담은 명곡"),
        Song(title="Drivers License", artist="Olivia Rodrigo", genre="Pop", reason="설레고 애틋한 감성"),
        Song(title="Treacherous", artist="Taylor Swift", genre="Pop/Country", reason="위험하게 설레는 감정"),
        Song(title="The 1", artist="Taylor Swift", genre="인디팝", reason="아련하고 설레는 감성"),
        Song(title="Die in a Beautiful Place", artist="Ethel Cain", genre="인디팝", reason="아름답게 빠져드는 설렘"),
    ],
    ("설렘", "보통", "R&B"): [
        Song(title="Adorn", artist="Miguel", genre="R&B", reason="부드럽게 빠져드는 설레는 사랑"),
        Song(title="Talk", artist="Khalid", genre="R&B/Pop", reason="설레는 첫 대화의 감성"),
        Song(title="Location", artist="Khalid", genre="R&B", reason="만나고 싶은 설레는 마음"),
        Song(title="No Scrubs", artist="TLC", genre="R&B", reason="솔직한 사랑의 감성"),
        Song(title="Slow Dance", artist="Anderson .Paak", genre="R&B", reason="느린 춤처럼 달콤한 설렘"),
    ],
    ("설렘", "보통", "인디"): [
        Song(title="Stolen Dance", artist="Milky Chance", genre="인디팝", reason="훔쳐간 춤처럼 달콤한 설렘"),
        Song(title="From Eden", artist="Hozier", genre="인디록/포크", reason="에덴동산 같은 아름다운 설렘"),
        Song(title="Riptide", artist="Vance Joy", genre="인디팝", reason="소용돌이처럼 빠져드는 설렘"),
        Song(title="I Found", artist="Amber Run", genre="인디팝", reason="찾아낸 사랑의 설레는 감성"),
        Song(title="Bloom", artist="The Paper Kites", genre="인디포크", reason="꽃처럼 피어나는 설렘"),
    ],
    ("설렘", "느림", "K-Pop"): [
        Song(title="Only Then", artist="폴킴", genre="K-Pop/발라드", reason="잔잔하게 설레는 고백송"),
        Song(title="밤편지", artist="IU", genre="K-Pop/인디", reason="포근하게 설레는 감성"),
        Song(title="사랑하기 때문에", artist="유재하", genre="K-Pop/발라드", reason="따뜻한 사랑을 담은 클래식"),
        Song(title="When We Were Young", artist="어반자카파", genre="K-Pop/R&B", reason="젊은 날의 설렘을 담은 곡"),
        Song(title="좋아", artist="DAY6", genre="K-Pop", reason="좋아하는 마음의 설레는 고백"),
    ],
    ("설렘", "느림", "J-Pop"): [
        Song(title="First Love", artist="宇多田ヒカル", genre="J-Pop/R&B", reason="첫사랑처럼 순수하고 설레는 곡"),
        Song(title="僕が君に恋をした", artist="あいみょん", genre="J-Pop", reason="사랑에 빠진 순간의 설렘"),
        Song(title="花", artist="ORANGE RANGE", genre="J-Pop", reason="꽃처럼 피어나는 아련한 설렘"),
        Song(title="白日", artist="King Gnu", genre="J-Pop/Rock", reason="하얀 낮처럼 순수한 설렘"),
        Song(title="あの夢をなぞって", artist="YOASOBI", genre="J-Pop", reason="꿈을 따라가는 설레는 감성"),
    ],
    ("설렘", "느림", "Pop"): [
        Song(title="A Thousand Years", artist="Christina Perri", genre="Pop", reason="영원한 설렘을 담은 명곡"),
        Song(title="Tenerife Sea", artist="Ed Sheeran", genre="Pop", reason="바다처럼 깊은 설렘"),
        Song(title="All of Me", artist="John Legend", genre="R&B/Pop", reason="온전한 사랑의 설렘"),
        Song(title="Can I Be Him", artist="James Arthur", genre="Pop", reason="조심스럽게 설레는 감정"),
        Song(title="Kiss Me", artist="Ed Sheeran", genre="Pop", reason="달콤하고 설레는 러브송"),
    ],
    ("설렘", "느림", "R&B"): [
        Song(title="Best Part", artist="Daniel Caesar ft. H.E.R.", genre="R&B/Soul", reason="가장 좋은 부분처럼 달콤한 설렘"),
        Song(title="Die With A Smile", artist="Lady Gaga & Bruno Mars", genre="Pop/R&B", reason="함께하고 싶은 설레는 마음"),
        Song(title="Slow Motion", artist="Trey Songz", genre="R&B", reason="천천히 빠져드는 설렘"),
        Song(title="No One", artist="Alicia Keys", genre="R&B/Soul", reason="오직 너뿐이라는 설레는 마음"),
        Song(title="Say Yes", artist="Michelle Williams ft. Beyoncé & Kelly Rowland", genre="R&B/Gospel", reason="함께하고 싶은 설레는 고백"),
    ],
    ("설렘", "느림", "인디"): [
        Song(title="Bloom", artist="The Paper Kites", genre="인디포크", reason="꽃처럼 피어나는 설렘"),
        Song(title="I Found", artist="Amber Run", genre="인디팝", reason="찾아낸 사랑의 감성"),
        Song(title="Lover, Please Stay", artist="Nothing But Thieves", genre="인디록", reason="머물러달라는 설레는 부탁"),
        Song(title="Suitcase", artist="Novo Amor", genre="인디포크", reason="함께 떠나고 싶은 설렘"),
        Song(title="All I Want", artist="Kodaline", genre="인디팝", reason="원하는 건 오직 하나뿐이라는 설렘"),
    ],

    # ── 피곤 ──────────────────────────────────────────────────
    ("피곤", "느림", "K-Pop"): [
        Song(title="가을 아침", artist="IU", genre="K-Pop/인디", reason="포근하게 지친 몸을 감싸주는 곡"),
        Song(title="Blueming", artist="IU", genre="K-Pop/인디", reason="나른하고 몽환적인 분위기"),
        Song(title="이 밤의 끝을 잡고", artist="성시경", genre="K-Pop/발라드", reason="지친 밤을 달래주는 곡"),
        Song(title="꽃갈피", artist="IU", genre="K-Pop", reason="편안하고 포근한 사운드"),
        Song(title="비가 오는 날엔", artist="다이나믹 듀오", genre="K-Pop/Hip-Hop", reason="쉬고 싶은 날에 딱 맞는 감성"),
    ],
    ("피곤", "느림", "J-Pop"): [
        Song(title="眠れぬ夜", artist="中島みゆき", genre="J-Pop", reason="잠 못 드는 밤을 함께하는 곡"),
        Song(title="やさしさに包まれたなら", artist="荒井由実", genre="J-Pop", reason="따뜻함에 감싸이는 포근한 곡"),
        Song(title="睡蓮花", artist="湘南乃風", genre="J-Pop/Reggae", reason="수련처럼 고요하게 쉬어가는 곡"),
        Song(title="春の歌", artist="スピッツ", genre="J-Pop", reason="봄 노래처럼 포근한 휴식"),
        Song(title="なごり雪", artist="イルカ", genre="J-Pop/포크", reason="눈처럼 잔잔하게 내려앉는 위로"),
    ],
    ("피곤", "느림", "Pop"): [
        Song(title="Weightless", artist="Marconi Union", genre="앰비언트", reason="과학적으로 스트레스를 줄여주는 곡"),
        Song(title="Holocene", artist="Bon Iver", genre="인디포크", reason="광활한 자연처럼 마음을 비워주는 곡"),
        Song(title="Gymnopédie No.1", artist="Erik Satie", genre="클래식", reason="나른하고 평온한 분위기"),
        Song(title="Clair de Lune", artist="Debussy", genre="클래식", reason="달빛처럼 부드러운 피아노"),
        Song(title="Sleep", artist="Max Richter", genre="현대 클래식", reason="잠을 위해 만들어진 음악"),
    ],
    ("피곤", "느림", "R&B"): [
        Song(title="Tired", artist="Beabadoobee", genre="인디/R&B", reason="피곤함을 그대로 담은 공감 가는 곡"),
        Song(title="Pink + White", artist="Frank Ocean", genre="R&B", reason="부드럽게 감싸주는 몽환적인 R&B"),
        Song(title="Novacane", artist="Frank Ocean", genre="R&B", reason="나른하고 몽환적인 분위기"),
        Song(title="Self Control", artist="Frank Ocean", genre="R&B", reason="잔잔하게 흘러가는 감성"),
        Song(title="Nights", artist="Frank Ocean", genre="R&B", reason="밤처럼 조용하고 감성적인 곡"),
    ],
    ("피곤", "느림", "인디"): [
        Song(title="Re: Stacks", artist="Bon Iver", genre="인디포크", reason="쌓인 피로를 달래주는 곡"),
        Song(title="Holocene", artist="Bon Iver", genre="인디포크", reason="광활하게 마음을 비워주는 곡"),
        Song(title="Lua", artist="Bright Eyes", genre="인디포크", reason="지친 밤의 솔직한 감성"),
        Song(title="Sleeping Sickness", artist="City and Colour", genre="인디포크", reason="잠들고 싶은 마음을 담은 곡"),
        Song(title="Slow Burn", artist="Kacey Musgraves", genre="인디컨트리", reason="천천히 타오르듯 쉬어가는 곡"),
    ],
    ("피곤", "보통", "K-Pop"): [
        Song(title="한숨", artist="IU", genre="K-Pop", reason="지친 마음을 어루만지는 곡"),
        Song(title="Spring Day", artist="BTS", genre="K-Pop", reason="긴 터널 끝의 빛 같은 곡"),
        Song(title="Through the Night", artist="IU", genre="K-Pop/인디", reason="밤을 함께 지새우는 감성"),
        Song(title="잠", artist="BTS", genre="K-Pop/힙합", reason="쉬고 싶은 마음을 담은 곡"),
        Song(title="오래된 노래", artist="오왠", genre="K-Pop/인디", reason="힐링되는 감성의 곡"),
    ],
    ("피곤", "보통", "J-Pop"): [
        Song(title="風の通り道", artist="久石譲", genre="J-Pop/영화음악", reason="바람이 지나가는 것처럼 편안한 곡"),
        Song(title="さよならの夏", artist="森山良子", genre="J-Pop", reason="여름 끝의 나른한 위로"),
        Song(title="Tomorrow never knows", artist="Mr.Children", genre="J-Pop/Rock", reason="내일은 알 수 없다는 위로"),
        Song(title="花火", artist="あいみょん", genre="J-Pop", reason="불꽃처럼 잠깐의 쉬어가는 시간"),
        Song(title="タイムマシーン", artist="back number", genre="J-Pop", reason="타임머신처럼 지친 일상을 잊게 해주는 곡"),
    ],
    ("피곤", "보통", "Pop"): [
        Song(title="Easy On Me", artist="Adele", genre="Pop", reason="부드럽게 감싸주는 곡"),
        Song(title="Let It Be", artist="The Beatles", genre="록", reason="놓아버리는 것도 괜찮다는 메시지"),
        Song(title="Better Place", artist="Rachel Platten", genre="Pop", reason="지쳐도 괜찮다는 위로"),
        Song(title="Slow Down", artist="Rudimental", genre="Pop/R&B", reason="쉬어가라는 메시지"),
        Song(title="Rest", artist="Troye Sivan", genre="인디팝", reason="쉬어도 괜찮다는 위로"),
    ],
    ("피곤", "보통", "R&B"): [
        Song(title="Superstar", artist="Sheryl Crow", genre="팝/R&B", reason="지친 나를 위한 따뜻한 위로"),
        Song(title="Tired", artist="Khalid", genre="R&B", reason="지침을 솔직하게 담은 곡"),
        Song(title="Water", artist="Tyla", genre="Afropop/R&B", reason="물처럼 부드럽게 흘러가는 곡"),
        Song(title="Sunday Morning", artist="Maroon 5", genre="Pop/R&B", reason="일요일 아침처럼 여유로운 곡"),
        Song(title="These Days", artist="Rudimental ft. Jess Glynne", genre="R&B/Pop", reason="요즘 같은 날들에 필요한 위로"),
    ],
    ("피곤", "보통", "인디"): [
        Song(title="Slow Burn", artist="Kacey Musgraves", genre="인디컨트리", reason="천천히 쉬어가도 된다는 메시지"),
        Song(title="Motion Picture Soundtrack", artist="Radiohead", genre="얼터너티브/인디", reason="영화 속처럼 조용한 휴식"),
        Song(title="Exhale", artist="Sabrina Carpenter", genre="팝/인디", reason="숨 내쉬듯 편안한 곡"),
        Song(title="Tired", artist="Beabadoobee", genre="인디록", reason="피곤함에 공감해주는 곡"),
        Song(title="Ribs", artist="Lorde", genre="인디팝", reason="지친 감정을 담담하게 담은 곡"),
    ],
    ("피곤", "빠름", "K-Pop"): [
        Song(title="에너제틱", artist="워너원", genre="K-Pop", reason="지친 몸에 에너지를 충전해주는 곡"),
        Song(title="IDOL", artist="BTS", genre="K-Pop/Hip-Hop", reason="자신을 사랑하게 해주는 에너지"),
        Song(title="Kick It", artist="NCT 127", genre="K-Pop", reason="강렬하게 깨어나게 하는 곡"),
        Song(title="Power", artist="EXO", genre="K-Pop", reason="힘을 주는 제목 그대로의 곡"),
        Song(title="빛", artist="EXO", genre="K-Pop", reason="어둠 속 빛을 찾아주는 곡"),
    ],
    ("피곤", "빠름", "J-Pop"): [
        Song(title="ギラギラ", artist="あいみょん", genre="J-Pop", reason="번쩍이는 에너지로 각성시키는 곡"),
        Song(title="紅蓮華", artist="LiSA", genre="J-Pop/애니", reason="불꽃처럼 타오르는 에너지"),
        Song(title="炎", artist="LiSA", genre="J-Pop/애니", reason="불꽃처럼 각성시키는 명곡"),
        Song(title="回してくれ", artist="sumika", genre="J-Pop", reason="신나는 에너지로 기분 전환"),
        Song(title="やってみよう", artist="WANIMA", genre="J-Pop/Punk", reason="해보자는 긍정 에너지"),
    ],
    ("피곤", "빠름", "Pop"): [
        Song(title="Eye of the Tiger", artist="Survivor", genre="록", reason="도전 정신을 불러일으키는 명곡"),
        Song(title="Roar", artist="Katy Perry", genre="Pop", reason="용기를 주는 응원가"),
        Song(title="Power", artist="Kanye West", genre="Hip-Hop", reason="강렬한 에너지 충전"),
        Song(title="Work Hard Play Hard", artist="Wiz Khalifa", genre="Hip-Hop", reason="열심히 살게 해주는 곡"),
        Song(title="Till I Collapse", artist="Eminem", genre="Hip-Hop", reason="한계를 넘게 해주는 에너지"),
    ],
    ("피곤", "빠름", "R&B"): [
        Song(title="Energy", artist="Beyoncé ft. Beam", genre="R&B/Hip-Hop", reason="에너지 그 자체인 비욘세의 곡"),
        Song(title="HUMBLE.", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="강렬한 에너지로 각성시키는 곡"),
        Song(title="Move", artist="Little Mix", genre="Pop/R&B", reason="움직이게 만드는 에너지"),
        Song(title="Partition", artist="Beyoncé", genre="R&B/Pop", reason="강렬한 에너지로 피로 날리는 곡"),
        Song(title="Run the World", artist="Beyoncé", genre="R&B/Pop", reason="세상을 지배하는 에너지"),
    ],
    ("피곤", "빠름", "인디"): [
        Song(title="Dog Days Are Over", artist="Florence + The Machine", genre="인디록", reason="힘든 날이 지나간다는 희망"),
        Song(title="Shake It Out", artist="Florence + The Machine", genre="인디록", reason="털어내고 다시 달리는 에너지"),
        Song(title="My Songs Know What You Did in the Dark", artist="Fall Out Boy", genre="팝펑크", reason="강렬하게 각성시키는 곡"),
        Song(title="Centuries", artist="Fall Out Boy", genre="팝펑크/인디", reason="역사에 남을 에너지"),
        Song(title="Mountain Sound", artist="Of Monsters and Men", genre="인디포크/록", reason="산처럼 강한 에너지"),
    ],

    # ── 집중 ──────────────────────────────────────────────────
    ("집중", "느림", "K-Pop"): [
        Song(title="가을 아침", artist="IU", genre="K-Pop/인디", reason="차분하고 집중되는 감성"),
        Song(title="봄날 (acoustic)", artist="BTS", genre="K-Pop/포크", reason="조용하고 감성적인 집중 모드"),
        Song(title="야생화", artist="박효신", genre="K-Pop/발라드", reason="감성적이지만 집중되는 분위기"),
        Song(title="공기 반 소리 반", artist="이적", genre="K-Pop", reason="조용하게 집중할 수 있는 분위기"),
        Song(title="Through the Night", artist="IU", genre="K-Pop/인디", reason="밤새 집중하게 해주는 곡"),
    ],
    ("집중", "느림", "J-Pop"): [
        Song(title="風の通り道", artist="久石譲", genre="J-Pop/영화음악", reason="지브리 감성의 집중 음악"),
        Song(title="いつも何度でも", artist="木村弓", genre="J-Pop/영화음악", reason="센과 치히로의 마법 같은 집중"),
        Song(title="となりのトトロ", artist="久石譲", genre="J-Pop/영화음악", reason="포근하고 집중되는 지브리 사운드"),
        Song(title="人生のメリーゴーランド", artist="久石譲", genre="J-Pop/영화음악", reason="하울의 움직이는 성 같은 몰입감"),
        Song(title="白日", artist="King Gnu", genre="J-Pop/Rock", reason="깊은 몰입감을 주는 명곡"),
    ],
    ("집중", "느림", "Pop"): [
        Song(title="Experience", artist="Ludovico Einaudi", genre="현대 클래식", reason="집중력을 높여주는 피아노 명곡"),
        Song(title="Time", artist="Hans Zimmer", genre="영화음악", reason="깊은 몰입을 이끄는 곡"),
        Song(title="Comptine d'un autre été", artist="Yann Tiersen", genre="현대 클래식", reason="아름다운 피아노로 집중 모드 ON"),
        Song(title="On the Nature of Daylight", artist="Max Richter", genre="현대 클래식", reason="고요한 집중의 시간"),
        Song(title="Interstellar Theme", artist="Hans Zimmer", genre="영화음악", reason="우주적인 몰입감"),
    ],
    ("집중", "느림", "R&B"): [
        Song(title="Pink + White", artist="Frank Ocean", genre="R&B", reason="몽환적이면서 집중되는 R&B"),
        Song(title="Self Control", artist="Frank Ocean", genre="R&B", reason="잔잔하게 흘러가며 집중하게 하는 곡"),
        Song(title="Ivy", artist="Frank Ocean", genre="R&B", reason="깊은 몰입감을 주는 감성"),
        Song(title="Nikes", artist="Frank Ocean", genre="R&B", reason="몽환적인 분위기로 집중 유도"),
        Song(title="Seigfried", artist="Frank Ocean", genre="R&B/인디", reason="깊이 있는 감성으로 몰입"),
    ],
    ("집중", "느림", "인디"): [
        Song(title="Holocene", artist="Bon Iver", genre="인디포크", reason="광활한 느낌의 깊은 몰입"),
        Song(title="Skinny Love", artist="Bon Iver", genre="인디포크", reason="조용하고 집중되는 인디 감성"),
        Song(title="Slow Burn", artist="Kacey Musgraves", genre="인디컨트리", reason="천천히 깊게 집중하게 해주는 곡"),
        Song(title="Death With Dignity", artist="Sufjan Stevens", genre="인디포크", reason="깊은 몰입감의 인디 명곡"),
        Song(title="Motion Picture Soundtrack", artist="Radiohead", genre="얼터너티브/인디", reason="영화처럼 깊게 빠져드는 감성"),
    ],
    ("집중", "보통", "K-Pop"): [
        Song(title="시작", artist="BTS", genre="K-Pop/힙합", reason="목표를 향해 나아가는 에너지"),
        Song(title="팔레트", artist="IU", genre="K-Pop", reason="여유 있게 집중하는 감성"),
        Song(title="열정", artist="자이언티", genre="K-Pop/R&B", reason="열정적으로 집중하게 해주는 곡"),
        Song(title="Outro: The Journey", artist="BTS", genre="K-Pop/힙합", reason="차분하게 집중하는 분위기"),
        Song(title="나는 나비", artist="전인권", genre="K-Pop/록", reason="자유롭게 집중하는 에너지"),
    ],
    ("집중", "보통", "J-Pop"): [
        Song(title="夜に駆ける", artist="YOASOBI", genre="J-Pop", reason="밤을 달리듯 집중하는 에너지"),
        Song(title="怪物", artist="YOASOBI", genre="J-Pop", reason="괴물처럼 강렬한 집중력"),
        Song(title="アイドル", artist="YOASOBI", genre="J-Pop", reason="빠르고 강렬한 집중 에너지"),
        Song(title="優しい彗星", artist="YOASOBI", genre="J-Pop", reason="혜성처럼 집중하는 감성"),
        Song(title="ハルジオン", artist="YOASOBI", genre="J-Pop", reason="봄 민들레처럼 집중하는 감성"),
    ],
    ("집중", "보통", "Pop"): [
        Song(title="Lose Yourself", artist="Eminem", genre="Hip-Hop", reason="최대 집중을 이끄는 명곡"),
        Song(title="The Middle", artist="Zedd", genre="일렉트로팝", reason="적당한 에너지로 집중 유지"),
        Song(title="Work", artist="Iggy Azalea", genre="Hip-Hop/팝", reason="작업 모드 ON"),
        Song(title="Hall of Fame", artist="The Script ft. will.i.am", genre="팝록", reason="명예의 전당을 향한 집중"),
        Song(title="Unstoppable", artist="Sia", genre="Pop", reason="멈출 수 없는 집중 에너지"),
    ],
    ("집중", "보통", "R&B"): [
        Song(title="HUMBLE.", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="강렬한 집중 에너지"),
        Song(title="Money Trees", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="깊은 몰입감의 K.Dot 명곡"),
        Song(title="Swimming Pools", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="중독성 있는 비트로 집중 유지"),
        Song(title="Alright", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="괜찮아진다는 메시지와 집중 에너지"),
        Song(title="Stressed Out", artist="twenty one pilots", genre="인디팝/R&B", reason="스트레스를 집중으로 승화"),
    ],
    ("집중", "보통", "인디"): [
        Song(title="Polaroid", artist="Imagine Dragons", genre="인디록", reason="감성적이면서 집중되는 인디록"),
        Song(title="Radioactive", artist="Imagine Dragons", genre="인디록", reason="강렬하게 집중시키는 에너지"),
        Song(title="Amsterdam", artist="Imagine Dragons", genre="인디록", reason="차분하면서 집중되는 감성"),
        Song(title="On Top of the World", artist="Imagine Dragons", genre="인디록", reason="세상 위의 집중 에너지"),
        Song(title="It's Time", artist="Imagine Dragons", genre="인디록", reason="이제 집중할 시간이라는 메시지"),
    ],
    ("집중", "빠름", "K-Pop"): [
        Song(title="피땀눈물", artist="BTS", genre="K-Pop/R&B", reason="강렬하게 집중하게 해주는 곡"),
        Song(title="DDU-DU DDU-DU", artist="블랙핑크", genre="K-Pop", reason="강렬하고 카리스마 있는 에너지"),
        Song(title="불꽃", artist="여자친구", genre="K-Pop", reason="불꽃처럼 타오르는 집중력"),
        Song(title="Black Swan", artist="BTS", genre="K-Pop/R&B", reason="예술적 몰입감을 주는 곡"),
        Song(title="한 (ONE)", artist="블랙핑크", genre="K-Pop", reason="강렬한 에너지로 집중 모드"),
    ],
    ("집중", "빠름", "J-Pop"): [
        Song(title="紅蓮華", artist="LiSA", genre="J-Pop/애니", reason="귀멸의 칼날처럼 강렬한 집중"),
        Song(title="炎", artist="LiSA", genre="J-Pop/애니", reason="불꽃처럼 타오르는 집중 에너지"),
        Song(title="廻廻奇譚", artist="Eve", genre="J-Pop/보카로", reason="주술회전처럼 강렬한 몰입"),
        Song(title="THE RUMBLING", artist="SiM", genre="J-Pop/메탈", reason="진격의 거인처럼 압도적인 집중"),
        Song(title="Cry Baby", artist="Official髭男dism", genre="J-Pop", reason="강렬하게 집중시키는 히게단 명곡"),
    ],
    ("집중", "빠름", "Pop"): [
        Song(title="Till I Collapse", artist="Eminem", genre="Hip-Hop", reason="극한의 집중 에너지"),
        Song(title="Can't Hold Us", artist="Macklemore", genre="Hip-Hop", reason="최고를 향한 집중"),
        Song(title="Stronger", artist="Kanye West", genre="Hip-Hop", reason="더 강해지려는 집중력"),
        Song(title="Power", artist="Kanye West", genre="Hip-Hop", reason="강력한 집중 모드"),
        Song(title="Eye of the Tiger", artist="Survivor", genre="록", reason="도전 정신으로 집중"),
    ],
    ("집중", "빠름", "R&B"): [
        Song(title="HUMBLE.", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="강렬한 집중 에너지의 명곡"),
        Song(title="Backseat Freestyle", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="빠르고 강렬한 집중"),
        Song(title="DNA.", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="DNA처럼 강렬한 집중 에너지"),
        Song(title="Black Panther", artist="Kendrick Lamar", genre="Hip-Hop/R&B", reason="블랙팬서처럼 강렬한 집중"),
        Song(title="King's Dead", artist="Jay Rock ft. Kendrick Lamar", genre="Hip-Hop/R&B", reason="강렬한 에너지의 콜라보"),
    ],
    ("집중", "빠름", "인디"): [
        Song(title="Radioactive", artist="Imagine Dragons", genre="인디록", reason="강렬하게 집중시키는 인디록"),
        Song(title="Thunder", artist="Imagine Dragons", genre="인디록", reason="천둥처럼 강렬한 집중 에너지"),
        Song(title="Natural", artist="Imagine Dragons", genre="인디록", reason="자연스럽게 집중하게 하는 에너지"),
        Song(title="Monster", artist="Imagine Dragons", genre="인디록", reason="괴물 같은 집중력을 불러오는 곡"),
        Song(title="Believer", artist="Imagine Dragons", genre="인디록", reason="믿음으로 집중하는 에너지"),
    ],
}

PLAYLIST_NAMES = {
    ("행복", "공부"): "✨ 공부도 신나게, 행복한 집중 시간",
    ("행복", "운동"): "💪 신나는 운동, 행복 에너지 폭발",
    ("행복", "드라이브"): "🚗 창문 열고 달리는 행복한 드라이브",
    ("행복", "휴식"): "☀️ 따뜻한 햇살 아래 행복한 휴식",
    ("행복", "작업"): "🎨 즐겁게 작업하는 행복한 시간",
    ("우울", "공부"): "📚 우울해도 괜찮아, 집중해봐",
    ("우울", "운동"): "🏃 땀 흘리며 털어내기",
    ("우울", "드라이브"): "🌧️ 빗속을 달리는 감성 드라이브",
    ("우울", "휴식"): "🛋️ 오늘은 그냥 쉬어도 돼",
    ("우울", "작업"): "🖤 감성적인 작업 시간",
    ("설렘", "공부"): "💭 그 사람 생각하며 공부하기",
    ("설렘", "운동"): "🌸 두근두근 설레는 운동 루틴",
    ("설렘", "드라이브"): "🌅 설레는 마음으로 달리는 드라이브",
    ("설렘", "휴식"): "💕 설레는 마음으로 여유롭게",
    ("설렘", "작업"): "✨ 설레는 마음으로 창작하기",
    ("피곤", "공부"): "😴 졸리지만 해내야 해, 집중 모드",
    ("피곤", "운동"): "⚡ 지쳐도 움직이는 힘",
    ("피곤", "드라이브"): "🌙 지친 하루 끝, 집으로 가는 길",
    ("피곤", "휴식"): "😌 오늘 충분히 수고했어",
    ("피곤", "작업"): "☕ 커피 한 잔 마시며 마무리",
    ("집중", "공부"): "🎯 몰입의 시간, 집중 모드 ON",
    ("집중", "운동"): "🔥 목표를 향해, 집중 운동",
    ("집중", "드라이브"): "🏎️ 목적지를 향해 달리는 집중 드라이브",
    ("집중", "휴식"): "🧘 마음을 비우는 집중 휴식",
    ("집중", "작업"): "💻 딥 포커스, 최고의 작업 시간",
}

DESCRIPTIONS = {
    "행복": "지금 이 행복한 순간을 더욱 빛나게 해줄 곡들을 모았어요 🎶",
    "우울": "오늘 하루 힘들었죠? 음악이 함께할게요 🫂",
    "설렘": "두근두근한 그 마음, 음악으로 함께해요 💓",
    "피곤": "지친 몸과 마음을 위한 플레이리스트예요. 잘 버텼어요 🌙",
    "집중": "방해 없이 몰입할 수 있도록, 최적의 곡들을 준비했어요 🎯",
}

GENRE_TAG_MAP = {
    "K-Pop": "🇰🇷 K-Pop",
    "J-Pop": "🇯🇵 J-Pop",
    "Pop": "🌍 Pop",
    "R&B": "🎷 R&B / Soul",
    "인디": "🎸 인디 / 얼터너티브",
}

@app.get("/")
def root():
    return {"message": "🎵 Music Mood Recommender API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: MoodRequest):
    key = (req.mood, req.tempo, req.genre)

    songs = SONG_DB.get(key)
    if not songs:
        # 장르 폴백: Pop으로
        fallback_key = (req.mood, req.tempo, "Pop")
        songs = SONG_DB.get(fallback_key, [])

    if not songs:
        all_songs = list(SONG_DB.values())
        songs = random.choice(all_songs)

    selected = random.sample(songs, min(5, len(songs)))

    playlist_key = (req.mood, req.activity)
    playlist_name = PLAYLIST_NAMES.get(playlist_key, f"🎵 {req.mood}한 {req.activity} 플레이리스트")
    description = DESCRIPTIONS.get(req.mood, "지금 기분에 맞는 곡들을 모았어요 🎵")
    genre_tag = GENRE_TAG_MAP.get(req.genre, req.genre)

    return RecommendResponse(
        playlist_name=playlist_name,
        description=description,
        genre_tag=genre_tag,
        songs=selected,
    )
