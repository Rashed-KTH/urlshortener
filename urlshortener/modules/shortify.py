import re
import uuid
import logging
from urlshortener.models import Urlshort
from django.shortcuts import render, get_object_or_404

SHORTIFY_MAXLENGTH = 250

#logging.basicConfig(filename = "D:/shortify.log",
#                    level = logging.DEBUG,
#                     format = '%(asctime)s %(levelname)s %(name)s %(message)s')


# Alphabet used in _url_id_encode.
#
# For better readability ignoring  0, o, O, l, I, 1, g & 9 values

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_LENGTH = len(ALPHABET)
SHORTIFY_ADDRESS = "http://rashed123.pythonanywhere.com/"

def url_shortener(url):
    """
    Create a shortened URL.
    IN: url -> URL to be shortened
    OUT: JSON string { short_url: "", url: "", message: "", status: "" }
    """
    short_url = ""

    if len(url) > SHORTIFY_MAXLENGTH:
        message = "The URL given exceeds the maximum of %d characters." % (settings.SHORTIFY_MAXLENGTH)
        status = "fail"

    elif url != "":
        match = re.match('[\w-]+://', url)

        if match is None:
            url = "http://" + url

        url_hash, short_url, message, status = _create_short_url(url)

    else:
        message = "No url specified."
        status = "fail"


    return {"short_url": short_url,
            "url": url,
            "message": message,
            "status": status }


def _create_short_url(url):
    """
    Fetch the URL hash for a URL if it exists or request a new URL hash
    IN: url -> URL to be shortened
    OUT: list [ url_hash, short_url, message, status ]

    """
    url_hash = ""
    short_url = ""
    try:
        available_url = Urlshort.objects.get(url=url.encode("utf8"))

        if available_url:
            url_hash = available_url.hash_value
    except:
        url_hash = _create_url_hash(url)

    #url_hash = "?hash=%s"%url_hash

    short_url =  SHORTIFY_ADDRESS + url_hash
    message = ""
    status = "success"

    return [url_hash, short_url, message, status]


def _create_url_hash(url):
    """
    Create and insert a new shortened URL into the database and return the hash.
    IN: url -> URL to be shortened
    OUT: URL Hash

    """
    try:
        url_obj = Urlshort.objects.create(hash_value="", url="")
        url_obj.save()
        url_obj = Urlshort.objects.latest("id")

        url_hash = _url_id_encode(url_obj.id)
        url_encoded = url.encode("utf8")
        Urlshort.objects.filter(id=url_obj.id).update(hash_value=url_hash, url=url_encoded)
    except :
        raise 
    
    return url_hash


def _url_id_encode(number):
    """
    Convert a base10 number to Base<ALPHABET_LENGTH> using the provided alphabet
    IN: number -> Base10 number to convert
    OUT: Base<ALPHABET_LENGTH> string

    """
    if (number >= 0 and number < ALPHABET_LENGTH):
        hash_value = _generate_hash(length=4)
        return ALPHABET[number] + hash_value

    encoded = ""

    while (number > 0):
        index   = number % ALPHABET_LENGTH
        number  = number // ALPHABET_LENGTH
        encoded = ALPHABET[index] + encoded

    return encoded

def _generate_hash(length):
    """
    generate a hash value for url id whose value is between 1 to ALPHABET_LENGTH.
    IN: desired hash length
    OUT: Hash value of specified length using python uuid package

    """
    hash_value = str(uuid.uuid4()) # Convert UUID format to a string
    hash_value = hash_value.replace("-","")
    return hash_value[0:length]
