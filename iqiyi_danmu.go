//modified from https://github.com/ycfather/sns-utilities/blob/master/src/compress/zlib/zlib_utils.go
package main

import (
    "bytes"
    "compress/zlib"
    "encoding/xml"
    "io/ioutil"
    "log"
    "net/http"
    "sort"
    "bufio"
    "os"
    "fmt"
    "strings"
)

type Result struct {
    Code string `xml:"code"`
    Dat  Data   `xml:"data"`
}

type Data struct {
    Entries []Entry `xml:"entry"`
}

type Entry struct {
    Int   int32      `xml:"int"`
    BList BulletList `xml:"list"`
}

type BulletList struct {
    Bullets []BulletInfo `xml:"bulletInfo"`
}

type BulletInfo struct {
    Id          string `xml:"contentId"`
    Content     string `xml:"content"`
    ShowTime    int32  `xml:"showTime"`
    AddTime     int32  `xml:"addTime"`
    Likes       int32  `xml:"likes"`
    Font        int32  `xml:"font"`
    Color       string `xml:"color"`
    Opacity     int32  `xml:"opacity"`
    Position    int32  `xml:"position"`
    Background  int32  `xml:"background"`
    ReplyUid    int32  `xml:"replyUid"`
    ContentType int32  `xml:"contentType"`
}

type ByInt []Entry

func (entries ByInt) Len() int           { return len(entries) }
func (entries ByInt) Swap(i, j int)      { entries[i], entries[j] = entries[j], entries[i] }
func (entries ByInt) Less(i, j int) bool { return entries[i].Int < entries[j].Int }

func main() {
    in_file := "tvID"
    fi, err := os.Open(in_file)
    defer fi.Close()
    if err != nil {
        fmt.Println(in_file, err)
        return
    }
    rd := bufio.NewReader(fi)
    for {
        line, err := rd.ReadString('\n')
        if err != nil {
            break
        }

        //get tvid
        line = strings.Replace(line, "\n", "", -1)
        ids := strings.Split(line, "\t")
        videoID := ids[0]
        tvID := ids[1]

        tvID_len := len(tvID)
        rs := []rune(tvID)
        part1 := string(rs[tvID_len-4 : tvID_len-2])
        part2 := string(rs[tvID_len-2 : tvID_len])

        //barrage out file name "videoID.danmu"
        outfile := fmt.Sprintf("%s.danmu", videoID)
        fout, err := os.Create(outfile)
        defer fout.Close()
        if err != nil {
            fmt.Println(outfile, err)
            return
        }

        log.Printf("Getting barrage of video: %s", videoID)
        for i := 1; i <= 300; i ++ {
            //buil barrage url
            barrage_url := fmt.Sprintf("http://cmts.iqiyi.com/bullet/%s/%s/%s_300_%d.z", part1, part2, tvID, i)

            response, err := http.Get(barrage_url)
            defer response.Body.Close()
            if err != nil {
                log.Fatalln("failed to get content from the specified url")
                break
            }

            //log.Printf("Content-Type : %s, Content-Length : %s\n", response.Header.Get("Content-Type"), response.Header.Get("Content-Length"))

            buf, err := ioutil.ReadAll(response.Body)
            if err != nil {
                log.Fatalln("failed to read response")
                break
            }

            zlib_buf := bytes.NewReader(buf)
            r, err := zlib.NewReader(zlib_buf)
            if err != nil {
                break
            }
            defer r.Close()

            str_buf, err := ioutil.ReadAll(r)
            //fmt.Println(string(str_buf))

            var result Result
            err = xml.Unmarshal(str_buf, &result)
            sort.Sort(ByInt(result.Dat.Entries))
            for _, entry := range result.Dat.Entries {
                for _, bullet := range entry.BList.Bullets {
                    barrage_info := fmt.Sprintf("%d\t%s\n", bullet.ShowTime, bullet.Content)
                    fout.WriteString(barrage_info)
                }
            }
        }
    }
}