from genericmetadata import GenericMetadata


class MetaDataStyle:
    BROWSE = 0
    INDEX = 1
    URL = 2

class WebComicScrapeIndex:

	def __init__():
        self.browse_pages = []
        self.num_pages = 0
        # check if file

    def write(location):
        pass
    
    def read(location):
        pass
    
    def addBrowseScrape(page,url,image,next=""):
        if page + 1 > self.num_pages:
            print "fffff'"
            return
        self.num_pages += 1

    def getBrowseScrapeLastPage:
        pass

    def getNumPages:
        pass


class WebComicTagPaths:
    pass

class WebComicTagImage:
    start = ""
    scrape_browse_regex_url = ""
    scrape_browse_regex_next = ""


class WebComicTagImage:


class RegexPart:
    maximum_matches = None
    reverse = None
    sort = None
    cut = None
    add_own = None
    regex = None

class WebComic:


	def __init__(cbw_file,cache_location="",auto_download_image=False):
        self.cbw_file = cbw_file
        self.cache.location = cache_location
        self.auto_download_image = auto_download_image
        self.scraper_index = WebComicScrapeIndex(location)
        self.has_meta = False
        self.scrape_index = False
        self.scrape_browse = False
        self.scrape_url = False
        self.cbw = None

    # LOAD
    
    def loadCBW():
        self.cbw = ET.parse(self.cbw_file)
        root_images = cbw.find('Images')
        if root_images:
            self.imagesCBW(root_images)
        root_info = cbw.find('Info')
        if root_info:
            self.infoCBW(root_info)

    def infoCBW(info):
        self.has_meta = True
        metadata = ComicInfoXml().convertXMLToMetadata(info)
        #metadata.pageCount = 0 # FIX THIS...
        return metadata

    def imagesCBW(images):
        for image_tag in images:
            if image_tag.tag == 'Image':
                try:
                    type = image_tag.attrib['Type']
                except:
                    type = "Unknown"
                
                try:
                    url =  image_tag.attrib['Url']
                except:
                    continue
    
                if type == "BrowseScraper" or url[0] == "?":
                    print "BrowseScraper"
                    
                    self.browserScrapeCBW(image_tag,url)
                
                elif type == "IndexScraper" or url[0] == "!":
                    print "IndexScraper"
                    self.indexCBW(image_tag,url)
                     
                elif type == "Url":
                    print "UrlScraper"
                    self.urlCBW(url)
                    
                elif:
                    print "ERROR"


    def partsCBW(image):
        parts = image.find('Parts')
        parts_list = []
        for part in parts:
            regex_part = RegexPart()
            if part.text == '' or part.text is None:
                continue
            
            regex_part.regex = HTMLParser.HTMLParser().unescape(part.text)
        
            try:
                regex_part.maximum_matches = part.attrib['MaximumMatches']
            except:
                pass
            try:
                regex_part.reverse = part.attrib['Reverse']
            except:
                pass
            try:
                regex_part.sort = part.attrib['Sort']
            except:
                pass
            try:
                regex_part.cut = part.attrib['Cut']
            except:
                pass
            try:
                regex_part.add_own = part.attrib['AddOwn']
            except:
                pass
            parts_list += [regex_part]
        return parts_list
    

    def browserScrapeCBW(image,url):
    
        self.partsCBW()
        if url[0] == "?":
            url = url[1:]
        url_split =  url.split('|')
        start = url_split[0]
        if len(url_split) == 3:
            image = url_split[1]
            nextpage = url_split[2]
        else:
        
        
        if self.auto_download_image
        pass

    def indexCBW(image):
        pass

    def urlCBW(image):
        pass
    
    


    def BrowseScrape():
        pass
  
    def IndexScrape(DownloadImage=False):
        pass
    
    def URLScrape():
        pass
        
    def Scrape(...):



            
    def getImage(page):
        #....
        
        if os.path.isfile(image_filename):
            try:
                with open(image_filename, 'rb') as image_file:
                    image_data = image_file.read()
            except:
                return self.getImageURL(page)
            try:
                Image.open(StringIO.StringIO(image_data))
            except:
                return self.getImageURL(page)
            return data
        else:
            return self.getImageURL(page)

    def getURL(url):
        """
        Loads URL with special headers to circumvent Forbidden 40X+
        """
        try:
            # Headers unblocks some forbidden pages
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
            response  = urllib2.urlopen(req)
            data = response.read()
        except:
            print "WebComic: [" + self.cbw + "] [" + url + "] Not found"
            return
            
    def getImageURL(page,url):
        """
        Loads an page from url an stores it to cache
        """
        iamge_data = getURL(url)
        if image_data is None:
            print "WebComic: [" + self.cbw + "] Page " + str(page) + " [" + url + "] Image not found"
            return
        try:
            image = Image.open(StringIO.StringIO(image_data))
            img_ext = image.format.lower()
        except:
            print "WebComic: [" + self.cbw + "] Page " + str(page) + " [" + url + "] Not an image"
            return
        try:
            image_filename = os.path.join(cache.location,str(page)+"."+img_ext)
            image_file = open(image_filename + ".tmp", 'w')
            image_file.write(image_data)
            image_file.close
            # such that we do not het partial images...
            os.rename(imagefilename + ".tmp",imagefilename)
        except:
            print "WebComic: [" + self.cbw + "] Page " + str(page) + " Could not write to " + image_filename
        return image_data
        