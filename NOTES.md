## Name
Bytelog.org

## Authors
Corey Matyas, Dylan Allbee, Vijay Atwater-Van Ness

## Links
http://kecebongsoft.com  
http://steveasleep.com  
https://zerokspot.com/weblog/2015/12/31/new-string-formatting-in-python/ - fonts?  
https://seanmckaybeck.com/scrapy-the-basics.html  
https://blog.ycombinator.com/basic-income  
http://purecss.io/layouts/blog/  
http://yes-www.org - outer border  
https://www.michaelfogleman.com  
http://www.2uo.de/ - Cool red colors  
http://idlewords.com/talks/website_obesity.htm#crisis - Code to text ratio
https://anadea.info/blog/how-to-choose-a-programming-language - Font

## Article Ideas
- Regular Expressions
- An opinion on when JS should, and shouldn't be used (and how)

## Features
- Twitter integration
- RSS feed
- content as compiled markdown files (tracked via github)
- browserstring page tracking?
- server-side syntax highlighting
- metadata parsing

## Implementation Details

### Content
Git hook -> Git Pull -> Parse Markdown -> Output file.jinja

### Browser Support
* IE11+
* Firefox (+Android)
* Chrome (+Android)
* Safari 9+ (+iOS)
* Opera (+Mobile)

### Assets
* Strictly PNG, use ZopfliPNG for compression. Exceptions for scalable (SVGZ) and animations (GIF)
* HTML, CSS, JavaScript should be minified. Combining assets is not necessary
* Raw JavaScript
* Scss +Bourbon
* Absolutely no inline styles, stylistic classes, or inline scripts
* Consider spritemapping for common images

## URL Schema
Rule: Url's with a trailing slash MUST be redirected with the slash removed.  
Rationale: A directory should be named in its plural form, and so the trailing slash is redundant.  

Example URLs
```
/projects
/projects/{:name}
/about
```

## Principles
1. Privacy is of the upmost importance.
2. Content:Code Ratio should be maximized. Put strain on the server, not the browser.
3. Javascript shall only add to user experience, never be a requirement.