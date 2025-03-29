CREATE MIGRATION m1h3lnmq4nlzhcbavrd3sanq6su7dilaeee3ip2262jla465hdk2aa
    ONTO m1zyjsahbds5sly4xbqycqi7j4rknlufh5s6vk3ljqxqbor2rmycrq
{
  CREATE ABSTRACT TYPE default::Votable {
      CREATE REQUIRED PROPERTY num_downvote: std::int32 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY num_upvote: std::int32 {
          SET default := 0;
      };
  };
  CREATE TYPE default::Rant EXTENDING default::Votable {
      CREATE REQUIRED PROPERTY body: std::str;
      CREATE REQUIRED PROPERTY category: std::str;
      CREATE REQUIRED PROPERTY created_at: std::datetime;
      CREATE REQUIRED PROPERTY geom: ext::postgis::geometry;
      CREATE REQUIRED PROPERTY title: std::str;
  };
  CREATE TYPE default::reply EXTENDING default::Votable {
      CREATE REQUIRED LINK parent_rant: default::Rant;
      CREATE REQUIRED PROPERTY body: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
  };
  DROP TYPE default::rant;
};
