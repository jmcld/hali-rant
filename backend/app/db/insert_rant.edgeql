INSERT Rant {
    title := <str>$title,
    body := <str>$body,
    geom := <ext::postgis::geometry>$geom,
    category := <str>$category,
    created_at := <datetime>$created_at,
}