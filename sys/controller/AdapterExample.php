<?php 
$root = $_SERVER['DOCUMENT_ROOT'];

    require_once $root . '/../sys/controller/PDO_Config.php';
    class PDOAdapter {
        public $conn = null;

        /**
        *   Connects to the database the moment we call this file
        */
        public function __construct(){
            try {
                $this->conn= new \PDO(DB_TYPE.':host='.DB_HOST.';dbname='.DB_NAME, DB_USER, DB_PASS);
                $this->conn->setAttribute(\PDO::ATTR_ERRMODE, \PDO::ERRMODE_EXCEPTION);
                //$this->conn->set_limit_time(60);
            }
            catch (\PDOException $e) {
                die('Failed to Connect' . $e->getMessage());
            }
            return $this->conn;
        }

        /*
        public function __destruct(){
            syslog(LOG_EMERG,"close connection yay");
        }
        */

        /**
        *   Closes the connection
        */
        public function closeConnection(){
            try{
                $this->conn = null;
            }catch(\PDOExceoption $e){
                die('Failed to close connection'. $e.getMessage());
            }
        }

       /**
        * [Function that can handle inserts,update & delete and returns row count with pre-defined Queries]
        * @param  [Query] $SQLquery [A query]
        * @return [int] $rows       [The number of rows in the result (default = 1)]
        */
        public function executeUpdate($SQLquery){
            try{
                $stmt = $this->conn->prepare($SQLquery);
                $stmt->execute();
                $rows= $stmt->rowCount();
                return $rows;
            }
            catch(\PDOException $e){
                //die('Failed to executeUpdate' . $e->getMessage());
                //throw new PDOException($e->getCode());
                return 0;
            }
        }

       /**
        * [Function that handle inserts,update & delete and returns row count with binding parameters]
        * @param  [Statement] $stmt [A Statement that is prepared to be executed]
        * @return [int] $rows       [The number of rows in the result (default = 1)]
        */
        public function executeUpdatePrepared($stmt){
            try{
                $stmt->execute();
                $rows= $stmt->rowCount();
                return $rows;
            }
            catch(\PDOException $e){
                die('Failed to executeUpdatePrepared' . $e->getMessage());
                throw new PDOException($e->getCode());
            }
        }

       /**
        * [Function that returns actual data with pre-defined queries]
        * @param  [Query] $SQLquery [A query]
        * @return [Array]           [An array of an array that contains the results]
        */
        public function executeFetch($SQLquery){
             try{
                $stmt = $this->conn->prepare($SQLquery);
                $stmt->execute();
                return $stmt->fetchAll();
            }
            catch(\PDOException $e){
                //die('Failed to executeFetch' . $e->getMessage());
                throw new PDOException($e->getCode());
            }
        }

       /**
        * [Function that returns actual data with preparedStatements with binding parameters]
        * @param  [Statement] $stmt [A Statement that is prepared to be executed]
        * @return [Array]       [An array of an array that contains the results]
        */
        public function executeFetchPrepared($stmt){
             try{
                $stmt->execute();
                return $stmt->fetchAll();
            }
            catch(\PDOException $e){
                //die('Failed to executeFetch' . $e->getMessage());
                throw new PDOException($e->getCode());
            }
        }
    }
?>
