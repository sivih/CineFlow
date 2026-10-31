import sqlite3
import os
from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'cineflow_premium_secure_key_2026'

app.secret_key = os.urandom(24)

DATABASE = os.path.join(os.path.dirname(__file__), 'cineflow.db')

SEED_MOVIES = [
    # ── Original entries ────────────────────────────────────────────────────
    {
        "title": "The Dark Knight",
        "genre": "Action / Crime",
        "release_year": 2008,
        "rating": 9.0,
        "description": (
            "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, "
            "Batman must accept one of the greatest psychological and physical tests of his ability "
            "to fight injustice. Heath Ledger's unforgettable portrayal of the Joker earned him a "
            "posthumous Academy Award and remains one of cinema's greatest performances of all time."
        ),
        "image_url": "https://images.unsplash.com/photo-1531259683007-016a7b628fc3?w=800&q=85",
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "duration": 152,
        "trailer_url": "https://www.youtube.com/embed/EXeTwQWrcwY",
        "featured": 1,
    },
    {
        "title": "Inception",
        "genre": "Sci-Fi / Thriller",
        "release_year": 2010,
        "rating": 8.8,
        "description": (
            "A skilled thief who steals corporate secrets through the use of dream-sharing technology "
            "is given the inverse task of planting an idea into the mind of a C.E.O. "
            "Christopher Nolan's mind-bending masterpiece challenges the boundaries of reality "
            "and features an iconic ensemble cast led by Leonardo DiCaprio."
        ),
        "image_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=85",
        "director": "Christopher Nolan",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "duration": 148,
        "trailer_url": "https://www.youtube.com/embed/YoHD9XEInc0",
        "featured": 1,
    },
    {
        "title": "Interstellar",
        "genre": "Sci-Fi / Adventure",
        "release_year": 2014,
        "rating": 8.6,
        "description": (
            "A team of explorers travel through a wormhole in space in an attempt to ensure "
            "humanity's survival. Directed by Christopher Nolan, Interstellar is a stunning "
            "visual and emotional journey that blends hard science fiction with a deeply human "
            "story about love, time, and sacrifice across galaxies."
        ),
        "image_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=800&q=85",
        "director": "Christopher Nolan",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "duration": 169,
        "trailer_url": "https://www.youtube.com/embed/zSWdZVtXT7E",
        "featured": 1,
    },
    {
        "title": "Parasite",
        "genre": "Drama / Thriller",
        "release_year": 2019,
        "rating": 8.5,
        "description": (
            "Greed and class discrimination threaten the newly formed symbiotic relationship between "
            "the wealthy Park family and the destitute Kim clan. Bong Joon-ho's Palme d'Or and "
            "Academy Award winning masterwork is a razor-sharp social satire that keeps audiences "
            "guessing until its shocking conclusion."
        ),
        "image_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&q=85",
        "director": "Bong Joon-ho",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "duration": 132,
        "trailer_url": "https://www.youtube.com/embed/5xH0HfJHsaY",
        "featured": 0,
    },
    {
        "title": "The Grand Budapest Hotel",
        "genre": "Comedy / Drama",
        "release_year": 2014,
        "rating": 8.1,
        "description": (
            "A writer encounters the owner of an aging European hotel between the wars and learns "
            "of his friendship with a young employee who becomes his most trusted confidant. "
            "Wes Anderson's visually magnificent film is a whimsical, witty, and warmly nostalgic "
            "adventure brimming with an all-star ensemble cast."
        ),
        "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=85",
        "director": "Wes Anderson",
        "cast": "Ralph Fiennes, Tony Revolori, Saoirse Ronan",
        "duration": 99,
        "trailer_url": "https://www.youtube.com/embed/1Fg5iWmQjwk",
        "featured": 0,
    },
    {
        "title": "Dune",
        "genre": "Sci-Fi / Epic",
        "release_year": 2021,
        "rating": 8.0,
        "description": (
            "Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his "
            "understanding, must travel to the most dangerous planet in the universe to ensure the "
            "future of his family and his people. Denis Villeneuve's sweeping adaptation of Frank "
            "Herbert's legendary novel is a breathtaking cinematic achievement."
        ),
        "image_url": "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=800&q=85",
        "director": "Denis Villeneuve",
        "cast": "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac",
        "duration": 155,
        "trailer_url": "https://www.youtube.com/embed/n9xhJrPXop4",
        "featured": 1,
    },
    {
        "title": "The Shawshank Redemption",
        "genre": "Drama",
        "release_year": 1994,
        "rating": 9.3,
        "description": (
            "Over the course of several years, two convicts form a friendship, seeking consolation "
            "and, eventually, redemption through basic compassion. Frank Darabont's timeless adaptation "
            "of Stephen King's novella is widely considered one of the greatest films ever made, "
            "a testament to the enduring power of hope."
        ),
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=85",
        "director": "Frank Darabont",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "duration": 142,
        "trailer_url": "https://www.youtube.com/embed/NmzuHjWmXOc",
        "featured": 1,
    },
    {
        "title": "Whiplash",
        "genre": "Drama / Music",
        "release_year": 2014,
        "rating": 8.5,
        "description": (
            "A promising young drummer enrolls at a cut-throat music conservatory where his "
            "pursuit of perfection is threatened by the erratic and potentially abusive "
            "instructor who will stop at nothing to realize a student's potential. "
            "Damien Chazelle's intense debut is an exhilarating and visceral experience."
        ),
        "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&q=85",
        "director": "Damien Chazelle",
        "cast": "Miles Teller, J.K. Simmons, Melissa Benoist",
        "duration": 107,
        "trailer_url": "https://www.youtube.com/embed/7d_jQycdQGo",
        "featured": 0,
    },
    {
        "title": "1917",
        "genre": "War / Drama",
        "release_year": 2019,
        "rating": 8.3,
        "description": (
            "At the height of World War I, two young British soldiers are given a seemingly "
            "impossible mission: deliver a message deep in enemy territory to call off a "
            "deadly attack on 1,600 men. Sam Mendes crafted this thrilling war epic to appear "
            "as one continuous unbroken shot, a technical and emotional masterpiece."
        ),
        "image_url": "https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=800&q=85",
        "director": "Sam Mendes",
        "cast": "George MacKay, Dean-Charles Chapman, Mark Strong",
        "duration": 119,
        "trailer_url": "https://www.youtube.com/embed/UcmZN0Mbl04",
        "featured": 0,
    },
    {
        "title": "Oppenheimer",
        "genre": "Biography / Drama",
        "release_year": 2023,
        "rating": 8.9,
        "description": (
            "The story of American scientist J. Robert Oppenheimer and his role in the development "
            "of the atomic bomb during World War II. Christopher Nolan's sprawling epic is a "
            "technically breathtaking and morally complex portrait of a man who forever changed "
            "the world, anchored by a towering performance from Cillian Murphy."
        ),
        "image_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&q=85",
        "director": "Christopher Nolan",
        "cast": "Cillian Murphy, Emily Blunt, Matt Damon",
        "duration": 180,
        "trailer_url": "https://www.youtube.com/embed/uYPbbksJxIg",
        "featured": 1,
    },
    {
        "title": "La La Land",
        "genre": "Romance / Musical",
        "release_year": 2016,
        "rating": 8.0,
        "description": (
            "While navigating their careers in Los Angeles, a pianist and an actress fall in love "
            "while attempting to reconcile their aspirations for the future. Damien Chazelle's "
            "dazzling musical is a love letter to dreamers everywhere, blending old Hollywood "
            "glamour with a modern, bittersweet emotional honesty."
        ),
        "image_url": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&q=85",
        "director": "Damien Chazelle",
        "cast": "Ryan Gosling, Emma Stone, John Legend",
        "duration": 128,
        "trailer_url": "https://www.youtube.com/embed/0pdqf4P9MB8",
        "featured": 0,
    },
    {
        "title": "Everything Everywhere All at Once",
        "genre": "Sci-Fi / Comedy",
        "release_year": 2022,
        "rating": 8.0,
        "description": (
            "An aging Chinese immigrant is swept up in an insane adventure in which she alone can "
            "save the world by exploring other universes connecting with the lives she could have "
            "led. The Daniels' genre-defying triumph swept the Academy Awards with seven wins "
            "including Best Picture."
        ),
        "image_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&q=85",
        "director": "Daniel Kwan, Daniel Scheinert",
        "cast": "Michelle Yeoh, Ke Huy Quan, Jamie Lee Curtis",
        "duration": 139,
        "trailer_url": "https://www.youtube.com/embed/wxN1T1uxQ2g",
        "featured": 0,
    },

    # ── NEW placeholder entries ──────────────────────────────────────────────
    {
        "title": "The Godfather",
        "genre": "Crime / Drama",
        "release_year": 1972,
        "rating": 9.2,
        "description": (
            "The aging patriarch of an organized crime dynasty transfers control of his clandestine "
            "empire to his reluctant son. Francis Ford Coppola's landmark film is a richly detailed "
            "portrait of power, loyalty, and family, widely considered one of the greatest movies "
            "ever made and the gold standard of American cinema."
        ),
        "image_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800&q=85",
        "director": "Francis Ford Coppola",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "duration": 175,
        "trailer_url": "https://www.youtube.com/embed/sY1S34973zA",
        "featured": 1,
    },
    {
        "title": "Blade Runner 2049",
        "genre": "Sci-Fi / Noir",
        "release_year": 2017,
        "rating": 8.0,
        "description": (
            "A young blade runner discovers a long-buried secret that has the potential to plunge "
            "what's left of society into chaos. Denis Villeneuve's visually stunning sequel expands "
            "the world of the original with meditative pacing, Roger Deakins' Oscar-winning "
            "cinematography, and profound questions about memory and identity."
        ),
        "image_url": "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800&q=85",
        "director": "Denis Villeneuve",
        "cast": "Ryan Gosling, Harrison Ford, Ana de Armas",
        "duration": 164,
        "trailer_url": "https://www.youtube.com/embed/gCcx85zbxz4",
        "featured": 0,
    },
    {
        "title": "Pulp Fiction",
        "genre": "Crime / Thriller",
        "release_year": 1994,
        "rating": 8.9,
        "description": (
            "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner "
            "bandits intertwine in four tales of violence and redemption. Quentin Tarantino's "
            "genre-defying masterpiece revolutionised independent cinema and remains one of the "
            "most influential films of the 20th century."
        ),
        "image_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=800&q=85",
        "director": "Quentin Tarantino",
        "cast": "John Travolta, Samuel L. Jackson, Uma Thurman",
        "duration": 154,
        "trailer_url": "https://www.youtube.com/embed/s7EdQ4FqbhY",
        "featured": 1,
    },
    {
        "title": "Spirited Away",
        "genre": "Animation / Fantasy",
        "release_year": 2001,
        "rating": 8.6,
        "description": (
            "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a "
            "world ruled by gods, spirits, and monsters, where humans are changed into beasts. "
            "Hayao Miyazaki's Academy Award-winning masterpiece is a richly imaginative and "
            "emotionally resonant fairy tale unlike anything else in animation."
        ),
        "image_url": "https://images.unsplash.com/photo-1551269901-5c5e14c25df7?w=800&q=85",
        "director": "Hayao Miyazaki",
        "cast": "Daveigh Chase, Suzanne Pleshette, Miyu Irino",
        "duration": 125,
        "trailer_url": "https://www.youtube.com/embed/ByXuk9QqQkk",
        "featured": 0,
    },
    {
        "title": "The Silence of the Lambs",
        "genre": "Thriller / Horror",
        "release_year": 1991,
        "rating": 8.6,
        "description": (
            "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal "
            "killer to help catch another serial killer, a madman who skins his victims. Jonathan "
            "Demme's chilling psychological thriller swept all five major Academy Awards — a feat "
            "achieved by only three films in history."
        ),
        "image_url": "https://images.unsplash.com/photo-1509281373149-e957c6296406?w=800&q=85",
        "director": "Jonathan Demme",
        "cast": "Jodie Foster, Anthony Hopkins, Scott Glenn",
        "duration": 118,
        "trailer_url": "https://www.youtube.com/embed/W6Mm8Sbe__o",
        "featured": 0,
    },
    {
        "title": "The Prestige",
        "genre": "Mystery / Thriller",
        "release_year": 2006,
        "rating": 8.5,
        "description": (
            "After a tragic accident, two stage magicians engage in a battle to create the ultimate "
            "illusion while sacrificing everything they have to outwit each other. Christopher "
            "Nolan's intricately plotted thriller is a dazzling puzzle box that rewards repeat "
            "viewings with hidden layers of meaning."
        ),
        "image_url": "https://images.unsplash.com/photo-1618519764620-7403abdbdfe9?w=800&q=85",
        "director": "Christopher Nolan",
        "cast": "Christian Bale, Hugh Jackman, Scarlett Johansson",
        "duration": 130,
        "trailer_url": "https://www.youtube.com/embed/RLtaA9fFFQA",
        "featured": 0,
    },
    {
        "title": "Mad Max: Fury Road",
        "genre": "Action / Adventure",
        "release_year": 2015,
        "rating": 8.1,
        "description": (
            "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search "
            "of her homeland with the aid of a group of female prisoners, a psychotic worshiper, "
            "and a drifter named Max. George Miller's relentless, visually extraordinary action "
            "epic won six Academy Awards and redefined the genre."
        ),
        "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=85",
        "director": "George Miller",
        "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult",
        "duration": 120,
        "trailer_url": "https://www.youtube.com/embed/hEJnMQG9ev8",
        "featured": 0,
    },
    {
        "title": "Arrival",
        "genre": "Sci-Fi / Drama",
        "release_year": 2016,
        "rating": 7.9,
        "description": (
            "A linguist works with the military to communicate with alien lifeforms after twelve "
            "mysterious spacecraft appear around the world. Denis Villeneuve's thoughtful, "
            "emotionally devastating science-fiction film is a meditation on language, time, "
            "and the choices that define us."
        ),
        "image_url": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800&q=85",
        "director": "Denis Villeneuve",
        "cast": "Amy Adams, Jeremy Renner, Forest Whitaker",
        "duration": 116,
        "trailer_url": "https://www.youtube.com/embed/tFMo3UJ4B4g",
        "featured": 0,
    },
    {
        "title": "No Country for Old Men",
        "genre": "Crime / Thriller",
        "release_year": 2007,
        "rating": 8.2,
        "description": (
            "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and "
            "more than two million dollars in cash near the Rio Grande. The Coen Brothers' "
            "haunting, Best Picture-winning neo-western is a masterclass in tension, silence, "
            "and the randomness of evil."
        ),
        "image_url": "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?w=800&q=85",
        "director": "Joel Coen, Ethan Coen",
        "cast": "Tommy Lee Jones, Javier Bardem, Josh Brolin",
        "duration": 122,
        "trailer_url": "https://www.youtube.com/embed/38A__WT3-o0",
        "featured": 0,
    },
    {
        "title": "Amélie",
        "genre": "Romance / Comedy",
        "release_year": 2001,
        "rating": 8.3,
        "description": (
            "Amélie is an innocent and naive girl in Paris with her own sense of justice. She "
            "decides to help those around her and, along the way, discovers love. Jean-Pierre "
            "Jeunet's whimsical French romantic comedy is a visually inventive, joyfully "
            "eccentric celebration of everyday magic and human connection."
        ),
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=85",
        "director": "Jean-Pierre Jeunet",
        "cast": "Audrey Tautou, Mathieu Kassovitz, Rufus",
        "duration": 122,
        "trailer_url": "https://www.youtube.com/embed/HtUH9z_Oey8",
        "featured": 0,
    },
    {
        "title": "Knives Out",
        "genre": "Mystery / Comedy",
        "release_year": 2019,
        "rating": 7.9,
        "description": (
            "A detective investigates the death of a patriarch of an eccentric, combative family. "
            "Rian Johnson's sharp, supremely entertaining whodunit is a lovingly crafted homage "
            "to the classic mystery genre, anchored by a star-studded ensemble and a breakout "
            "performance from Ana de Armas."
        ),
        "image_url": "https://images.unsplash.com/photo-1575908539614-ff89490f4a78?w=800&q=85",
        "director": "Rian Johnson",
        "cast": "Daniel Craig, Chris Evans, Ana de Armas",
        "duration": 130,
        "trailer_url": "https://www.youtube.com/embed/qGqiHJTsRkQ",
        "featured": 0,
    },
    {
        "title": "Portrait of a Lady on Fire",
        "genre": "Romance / Drama",
        "release_year": 2019,
        "rating": 8.1,
        "description": (
            "On an isolated island in Brittany at the end of the eighteenth century, a female "
            "painter is obliged to paint a wedding portrait of a young woman. Céline Sciamma's "
            "achingly beautiful and intensely felt period drama is a meditation on gaze, art, "
            "memory, and the fleeting nature of love."
        ),
        "image_url": "https://images.unsplash.com/photo-1579762715118-a6f1d4b934f1?w=800&q=85",
        "director": "Céline Sciamma",
        "cast": "Noémie Merlant, Adèle Haenel, Luàna Bajrami",
        "duration": 122,
        "trailer_url": "https://www.youtube.com/embed/2FZUkSqhpzQ",
        "featured": 0,
    },
    {
        "title": "The Lighthouse",
        "genre": "Horror / Drama",
        "release_year": 2019,
        "rating": 7.5,
        "description": (
            "Two lighthouse keepers try to maintain their sanity while living on a remote and "
            "mysterious New England island in the 1890s. Robert Eggers' hypnotic, claustrophobic "
            "psychological horror — shot in stark black-and-white — is a fever dream of maritime "
            "myth and madness featuring two career-best performances."
        ),
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=85",
        "director": "Robert Eggers",
        "cast": "Robert Pattinson, Willem Dafoe",
        "duration": 109,
        "trailer_url": "https://www.youtube.com/embed/Hyag7lR8CPA",
        "featured": 0,
    },  {
        "title": "Breaking Bad",
        "genre": "Crime / Drama",
        "release_year": 2008,
        "rating": 9.5,
        "description": (
            "A high school chemistry teacher diagnosed with inoperable lung cancer turns to a "
            "life of crime, manufacturing and selling methamphetamine with a former student to "
            "secure his family's financial future. Widely regarded as one of the greatest "
            "television series of all time."
        ),
        "image_url": "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=800&q=85",
        "director": "Vince Gilligan",
        "cast": "Bryan Cranston, Aaron Paul, Anna Gunn",
        "duration": 49,
        "trailer_url": "https://www.youtube.com/embed/HhesaQXLuRY",
        "featured": 1,
    },
    {
        "title": "Stranger Things",
        "genre": "Sci-Fi / Horror",
        "release_year": 2016,
        "rating": 8.7,
        "description": (
            "When a young boy vanishes from a small Indiana town, his friends uncover a secret "
            "government lab, a gateway to an alternate dimension, and a sinister girl with "
            "telekinetic powers. A nostalgic, thrilling homage to 1980s supernatural cinema."
        ),
        "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=85",
        "director": "The Duffer Brothers",
        "cast": "Millie Bobby Brown, Finn Wolfhard, Winona Ryder",
        "duration": 51,
        "trailer_url": "https://www.youtube.com/embed/b9EkMc79ZSU",
        "featured": 1,
    },
    {
        "title": "Chernobyl",
        "genre": "Drama / History",
        "release_year": 2019,
        "rating": 9.4,
        "description": (
            "In April 1986, a huge explosion erupted at the Chernobyl nuclear power plant in northern "
            "Ukraine. This gripping miniseries follows the stories of the brave men and women who "
            "sacrificed themselves to save Europe from an unimaginable disaster."
        ),
        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=85",
        "director": "Johan Renck",
        "cast": "Jared Harris, Stellan Skarsgård, Emily Watson",
        "duration": 330,
        "trailer_url": "https://www.youtube.com/embed/s9APLXM9Ei8",
        "featured": 0,
    },
    {
        "title": "Succession",
        "genre": "Drama / Satire",
        "release_year": 2018,
        "rating": 8.9,
        "description": (
            "The Roy family is known for controlling the biggest media and entertainment company in "
            "the world. However, their world changes when their father steps down. A cutthroat, "
            "brilliantly written look at wealth, power, and dysfunctional family dynamics."
        ),
        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=85",
        "director": "Jesse Armstrong",
        "cast": "Brian Cox, Jeremy Strong, Sarah Snook",
        "duration": 60,
        "trailer_url": "https://www.youtube.com/embed/OzYxJV_b3t8",
        "featured": 0,
    },
    {
        "title": "Sherlock",
        "genre": "Mystery / Crime",
        "release_year": 2010,
        "rating": 9.1,
        "description": (
            "A modern update finds the famous sleuth and his doctor partner solving crime in "
            "21st-century London. Benedict Cumberbatch's eccentric, sharp portrayal of Holmes "
            "makes this stylish adaptation an absolute standout masterpiece."
        ),
        "image_url": "https://images.unsplash.com/photo-1513757378314-e46255f6ed16?w=800&q=85",
        "director": "Mark Gatiss, Steven Moffat",
        "cast": "Benedict Cumberbatch, Martin Freeman, Una Stubbs",
        "duration": 90,
        "trailer_url": "https://www.youtube.com/embed/xK7S9mrFWL4",
        "featured": 0,
    },
]


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS movies")

        # 2. CREATE MOVIES TABLE
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS movies
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           title
                           TEXT
                           NOT
                           NULL,
                           genre
                           TEXT
                           NOT
                           NULL,
                           release_year
                           INTEGER
                           NOT
                           NULL,
                           rating
                           REAL
                           NOT
                           NULL,
                           description
                           TEXT
                           NOT
                           NULL,
                           image_url
                           TEXT
                           NOT
                           NULL,
                           director
                           TEXT
                           DEFAULT
                           '',
                           cast
                           TEXT
                           DEFAULT
                           '',
                           duration
                           INTEGER
                           DEFAULT
                           0,
                           trailer_url
                           TEXT
                           DEFAULT
                           '',
                           featured
                           INTEGER
                           DEFAULT
                           0
                       )
                       """)

        # 3. SEED THE NEW LARGE COLLECTION

        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]

        if count == 0:
            for m in SEED_MOVIES:
                cursor.execute("""
                               INSERT INTO movies (title, genre, release_year, rating, description,
                                                   image_url, director, cast, duration, trailer_url, featured)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """, (
                                   m["title"], m["genre"], m["release_year"], m["rating"], m["description"],
                                   m["image_url"], m["director"], m["cast"], m["duration"], m["trailer_url"],
                                   m["featured"]
                               ))
            conn.commit()
            print(f"[CineFlow] Database successfully populated with {len(SEED_MOVIES)} movies!")
        else:
            print(f"[CineFlow] Database already contains {count} movies — skipping seed.")

        # 2. CREATE USERS TABLE
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           username
                           TEXT
                           NOT
                           NULL
                           UNIQUE,
                           email
                           TEXT
                           NOT
                           NULL
                           UNIQUE,
                           password
                           TEXT
                           NOT
                           NULL,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       """)

        # 3. CREATE REVIEWS TABLE
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS reviews
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           movie_id
                           INTEGER
                           NOT
                           NULL,
                           username
                           TEXT
                           NOT
                           NULL,
                           rating
                           INTEGER
                           NOT
                           NULL,
                           comment
                           TEXT
                           NOT
                           NULL,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           FOREIGN
                           KEY
                       (
                           movie_id
                       ) REFERENCES movies
                       (
                           id
                       )
                           )
                       """)
        conn.commit()

        # Add new columns to existing databases
        for col, definition in [
            ("director", "TEXT DEFAULT ''"),
            ("cast", "TEXT DEFAULT ''"),
            ("duration", "INTEGER DEFAULT 0"),
            ("trailer_url", "TEXT DEFAULT ''"),
            ("featured", "INTEGER DEFAULT 0"),
        ]:
            try:
                cursor.execute(f"ALTER TABLE movies ADD COLUMN {col} {definition}")
                conn.commit()
            except sqlite3.OperationalError:
                pass

        cursor.execute("SELECT COUNT(*) AS cnt FROM movies")
        count = cursor.fetchone()["cnt"]

        if count == 0:
            cursor.executemany(
                """
                INSERT INTO movies
                (title, genre, release_year, rating, description,
                 image_url, director, cast, duration, trailer_url, featured)
                VALUES (:title, :genre, :release_year, :rating, :description,
                        :image_url, :director, :cast, :duration, :trailer_url, :featured)
                """,
                SEED_MOVIES,
            )
            conn.commit()
            print(f"[CineFlow] Database seeded with {len(SEED_MOVIES)} movies.")
        else:
            print(f"[CineFlow] Database already contains {count} movies — skipping seed.")


@app.route("/")
def index():
    db = get_db()

    # 1. Query all movies for your library grid
    all_movies = db.execute("SELECT * FROM movies").fetchall()

    # 2. Query and build the list of distinct genres for your filter buttons
    genres_raw = db.execute("SELECT DISTINCT genre FROM movies").fetchall()
    genres = [r["genre"] for r in genres_raw]

    # 3. Calculate metrics for your sub-header statistics
    stats = {
        "total": db.execute("SELECT COUNT(*) FROM movies").fetchone()[0],
        "genres": db.execute("SELECT COUNT(DISTINCT genre) FROM movies").fetchone()[0],
        "avg": round(db.execute("SELECT AVG(rating) FROM movies").fetchone()[0] or 0, 1),
    }

    # 4. Safely return everything to index.html
    return render_template(
        "index.html",
        movies=all_movies,
        genres=genres,
        stats=stats
    )
@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if movie is None:
        return render_template("404.html"), 404

    related = db.execute(
        "SELECT id, title, genre, release_year, rating, image_url "
        "FROM movies WHERE genre = ? AND id != ? ORDER BY rating DESC LIMIT 4",
        (movie["genre"], movie_id),
    ).fetchall()

    if len(related) < 3:
        ids_exclude = [movie_id] + [r["id"] for r in related]
        placeholders = ",".join("?" * len(ids_exclude))
        extra = db.execute(
            f"SELECT id, title, genre, release_year, rating, image_url "
            f"FROM movies WHERE id NOT IN ({placeholders}) ORDER BY rating DESC LIMIT 4",
            ids_exclude,
        ).fetchall()
        related = list(related) + list(extra)

    return render_template("movie_detail.html", movie=movie, related=related[:4])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/joinus")
def joinus():
    return render_template("joinus.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")



from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        # 2. Use check_password_hash instead of "== password"
        if user and check_password_hash(user["password"], password):
            # Set session tokens to switch state to Logged-In
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]

            return redirect(url_for("profile"))
        else:
            flash("Invalid email address or password combination.", "error")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            return "Please fill out all fields.", 400

        db = get_db()
        existing_user = db.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?", (username, email)
        ).fetchone()

        if existing_user:
            return "Username or Email already registered!", 400

        hashed_password = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        db.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/profile")
def profile():

    if "user_id" not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))

    db = get_db()

    user_data = {
        "username": session["username"],
        "email": session["email"]
    }

    return render_template("profile.html", user=user_data)
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    genre = request.args.get("genre", "").strip()
    sort = request.args.get("sort", "rating").strip()

    sort_map = {
        "rating": "rating DESC",
        "year_desc": "release_year DESC",
        "year_asc": "release_year ASC",
        "title": "title ASC",
    }
    order = sort_map.get(sort, "rating DESC")

    db = get_db()
    params = []
    conditions = []

    if query:
        conditions.append("(title LIKE ? OR genre LIKE ? OR director LIKE ?)")
        params += [f"%{query}%", f"%{query}%", f"%{query}%"]
    if genre:
        conditions.append("genre LIKE ?")
        params.append(f"%{genre}%")

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    movies = db.execute(
        f"SELECT id, title, genre, release_year, rating, image_url, director, duration "
        f"FROM movies {where} ORDER BY {order}",
        params,
    ).fetchall()

    genres_raw = db.execute("SELECT DISTINCT genre FROM movies ORDER BY genre").fetchall()
    genres = [r["genre"] for r in genres_raw]

    return render_template("search.html",
                           movies=movies,
                           query=query,
                           genre=genre,
                           sort=sort,
                           genres=genres)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)