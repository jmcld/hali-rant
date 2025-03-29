CREATE MIGRATION m1zyjsahbds5sly4xbqycqi7j4rknlufh5s6vk3ljqxqbor2rmycrq
    ONTO m1sg5xzfaderbvmluplpcbkoo3szgpplbkp2ciwzof2cebaxwtrtgq
{
  ALTER TYPE default::rant {
      ALTER PROPERTY geom {
          SET TYPE ext::postgis::geometry USING (<ext::postgis::geometry>.geom);
      };
  };
};
