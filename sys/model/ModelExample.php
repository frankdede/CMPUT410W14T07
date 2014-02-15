<?php

/**
 *  Model class for a Clinic
 */
class Clinic implements JsonSerializable{

    private $clinicName;
    private $clinicId;
    private $clinicAddress;
    private $clinicCity;
    private $clinicProvince;
    private $clinicPostalCode;
    private $latitude;
    private $longtitude;
    private $clinicEmail;
    private $website;
    private $contactPerson;
    private $phone;
    private $active;
    private $expiration;

    /**
     * Populate every field in Clinic object
     * @param [Array] $p_info_array [Array with all information on Clinic]
     */
    public function setInfo($p_info_array) {
        $this->setName($p_info_array['name']);
        $this->setId($p_info_array['clinic_id']);
        $this->setAddress($p_info_array['address']);
        $this->setCity($p_info_array['city']);
        $this->setProvince($p_info_array['province']);
        $this->setPostalCode($p_info_array['postal_code']);
        $this->setLatitude($p_info_array['latitude']);
        $this->setLongtitude($p_info_array['longtitude']);
        $this->setEmail($p_info_array['email']);
        $this->setWebsite($p_info_array['website']);
        $this->setContactPerson($p_info_array['contact_person']);
        $this->setPhone($p_info_array['phone']);
        $this->setActive($p_info_array['active']);
        $this->setExpirationDate($p_info_array['expiration']);
    }

    /**
     * Getters
     */
    public function getName() {
        return $this->clinicName;
    }
    public function getId() {
        return $this->clinicId;
    }
    public function getAddress() {
        return $this->clinicAddress;
    }
    public function getCity() {
        return $this->clinicCity;
    }
    public function getProvince() {
        return $this->clinicProvince;
    }
    public function getPostalCode() {
        return $this->clinicPostalCode;
    }
    public function getLatitude() {
        return $this->latitude;
    }
    public function getLongtitude() {
        return $this->longtitude;
    }
    public function getEmail() {
        return $this->clinicEmail;
    }
    public function getWebsite() {
        return $this->website;
    }
    public function getContactPerson() {
        return $this->contactPerson;
    }
    public function getPhone(){
        return $this->phone;
    }
    public function getActive() {
        return $this->active;
    }
    public function getExpirationDate() {
        return $this->expiration;
    }


    /**
     * Setters
     */
    public function setName($p_clinic_name) {
        $this->clinicName = $p_clinic_name;
    }
    public function setId($p_clinic_id) {
        $this->clinicId = $p_clinic_id;
    }
    public function setAddress($p_clinic_address) {
        $this->clinicAddress =  $p_clinic_address;
    }
    public function setCity($p_clinic_city) {
        $this->clinicCity = $p_clinic_city;
    }
    public function setProvince($p_clinic_province) {
        $this->clinicProvince = $p_clinic_province;
    }
    public function setPostalCode($p_clinic_postal_code) {
        $this->clinicPostalCode = $p_clinic_postal_code;
    }
    public function setLatitude($p_latitude) {
        $this->latitude = $p_latitude;
    }
    public function setLongtitude($p_longtitude) {
        $this->longtitude = $p_longtitude;
    }
    public function setEmail($p_clinic_email) {
        $this->clinicEmail = $p_clinic_email;
    }
    public function setWebsite($p_website) {
        $this->website = $p_website;
    }
    public function setContactPerson($p_contact_person) {
        $this->contactPerson = $p_contact_person;
    }
    public function setPhone($p_phone){
        $this->phone = $p_phone;
    }
    public function setActive($p_active) {
        $this->active = $p_active;
    }
    public function setExpirationDate($p_expiration){
        $this->expiration = $p_expiration;
    }

    /**
     * Data to be serialized into JSON
     * @return Array
     */
    public function jsonSerialize() {
        return array(
            'clinicName' => $this->clinicName,
            'clinicId' => $this->clinicId,
            'clinicAddress' => $this->clinicAddress,
            'clinicCity' => $this->clinicCity,
            'clinicProvince' => $this->clinicProvince,
            'clinicPostalCode' => $this->clinicPostalCode,
            'latitude' => $this->latitude,
            'longtitude' => $this->longtitude,
            'clinicEmail' => $this->clinicEmail,
            'website' => $this->website,
            'contactPerson' => $this->contactPerson,
            'phone' => $this->phone,
            'active' => $this->active,
            'expiration' => $this->expiration
        );
    }
}
?>
