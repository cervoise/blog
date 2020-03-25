# About anti XSS filter

Publication: 01/13/2013

An URL filter is a way to prevent XSS. I know some examples: IE8, the Netcraft Toolbar. Some CMS use the same kind of filter for XSS prevention like in PrestaShop. In all cases, they use regex, and then, there are two problems:

On the first hand, sometimes it can be bypass with some tricks. It’s happend in [IE8 a few years ago](https://www.whitehatsec.com/blog/internet-explorer-xss-filter/).

On the otherhand, it’s a protection based on a words/expressions list. If you omit some cases, or if some cases appear (for example with a new version of HTML, like HTML 5), you’re screwed. For those who are looking for a list of these events I found [this](http://help.dottoro.com/larrqqck.php) but I didn’t find an official list on W3C website (if someone got it, please send it).

The omission happened a few months ago in Netcraft Anti XSS filter. Indeed, Netcraft Toolbar uses a little database. Two events wasn’t cover in version 1.5: *onhachchange* and *oninput* events. This problem has been corrected in version 1.6.

It also happened in PrestaShop CMS. In this case, XSS filter is *isCleanHtml* method, from *Validate* class (*prestashop/classes/Validate.php*).

Comments about the function:

```php
/**
* Check for HTML field validity (no XSS please !)
*
* @param string $html HTML field to validate
* @return boolean Validity is ok or not
*/
```

The filter in version 1.4.7.3:

```javascript
public static function isCleanHtml($html)
{
    $jsEvent = 'onmousedown|onmousemove|onmmouseup|onmouseover|onmouseout|onload|onunload|onfocus|onblur|onchange|onsubmit|ondblclick|onclick|onkeydown|onkeyup|onkeypress|onmouseenter|onmouseleave|onerror';
    return (!preg_match('/<[ \t\n]*script/i', $html) && !preg_match('/<!--?.*('.$jsEvent.')[ \t\n]*=/i', $html)  && !preg_match('/.*script\:/i', $html));<br ?-->   }
```

```javascript
public static function isCleanHtml($html)
{
    $events = 'onmousedown|onmousemove|onmmouseup|onmouseover|onmouseout|onload|onunload|onfocus|onblur|onchange|onsubmit|ondblclick|onclick|onkeydown|onkeyup|onkeypress|onmouseenter|onmouseleave|onerror|onselect|onreset|onabort|ondragdrop|onresize|onactivate|onafterprint|onmoveend|onafterupdate|onbeforeactivate|onbeforecopy|onbeforecut|onbeforedeactivate|onbeforeeditfocus|onbeforepaste|onbeforeprint|onbeforeunload|onbeforeupdate|onmove|onbounce|oncellchange|oncontextmenu|oncontrolselect|oncopy|oncut|ondataavailable|ondatasetchanged|ondatasetcomplete|ondeactivate|ondrag|ondragend|ondragenter|onmousewheel|ondragleave|ondragover|ondragstart|ondrop|onerrorupdate|onfilterchange|onfinish|onfocusin|onfocusout|onhashchange|onhelp|oninput|onlosecapture|onmessage|onmouseup|onmovestart|onoffline|ononline|onpaste|onpropertychange|onreadystatechange|onresizeend|onresizestart|onrowenter|onrowexit|onrowsdelete|onrowsinserted|onscroll|onsearch|onselectionchange|onselectstart|onstart|onstop';
    return (!preg_match('/<[ \t\n]*script/i', $html) && !preg_match('/<!--?.*('.$events.')[ \t\n]*=/i', $html) && !preg_match('/.*script\:/i', $html));<br ?--> }
```

1.4.8.0 and 1.4.8.1 versions are not available on http://www.prestashop.com/en/versions-developpeurs and there’s nothing about this correction in changelog.

These kind of filter are bad because based on JS expression and if a field allows HTML injection, you still can inject some *iframe* or other HTML code (for phishing for example).

These two cases show that a filter based on regex must be well implemented and updated as the language you use! That was just for remind you that regex filters aren’t the solution and also talking about security correction silently implemented by editors.
